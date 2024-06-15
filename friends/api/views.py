from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils import st
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import User
from friends.models import FriendRequest
from friends.api.serializers import FriendRequestSerializer, SendFrientRequestSerializer
from rest_framework.exceptions import ValidationError
import constants as const
from accounts.api.serializer import UserListSerializer


class SendFriendRequest(APIView):
    """
    View to handle sending a friend request.

    This view handles POST requests to send a friend request. It uses the `SendFrientRequestSerializer`
    to validate and create a new friend request. The view returns appropriate responses based on the success
    or failure of the request. 
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):

        try:
            serializer = SendFrientRequestSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            payload = st.get_payload(
                detail=serializer.data,
                message="Friend request sent successfully.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            error_message = st.custome_message(error=e)
            payload = st.get_payload(
                detail={},
                message=error_message,
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            payload = st.get_payload(
                detail={},
                message="Object doesn't exists.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("New error: : ", e)
            payload = st.get_payload(
                detail={},
                message="An un-expected error Occurse.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(data=payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AcceptFriendRequestView(APIView):
    """
    View to handle accepting a friend request.

    This view handles POST requests to accept a friend request. It checks the provided request ID,
    verifies the status of the friend request, and updates its status to 'accepted' if valid. 
    The view returns appropriate responses based on the success or failure of the request.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        request_id = request.data.get("request_id")
        if not request_id:
            payload = st.get_payload(
                detail={},
                message="Request ID is required.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            friend_request = FriendRequest.objects.get(
                from_user=request_id, to_user=request.user
            )
            if friend_request.status == const.ACCEPTED:
                payload = st.get_payload(
                    detail={},
                    message="Friend request already accepted.",
                    is_authenticated=st.is_authenticated_status(request),
                )
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            friend_request.status = const.ACCEPTED
            friend_request.save()

            payload = st.get_payload(
                detail={},
                message="Friend request accepted.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_200_OK)

        except FriendRequest.DoesNotExist:
            payload = st.get_payload(
                detail={},
                message="Friend request not found.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:

            payload = st.get_payload(
                detail={},
                message=f"{e}",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            payload = st.get_payload(
                detail={},
                message="An unexpected error occurred.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RejectFriendRequestView(APIView):
    """
    View to handle rejecting a friend request.

    This view handles POST requests to reject a friend request. It validates the provided request ID,
    checks the status of the friend request, and updates its status to 'rejected' if valid. 
    The view returns appropriate responses based on the success or failure of the request.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        request_id = request.data.get("request_id")
        if not request_id:
            payload = st.get_payload(
                detail={},
                message="Request ID is required.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            friend_request = FriendRequest.objects.get(
                from_user=request_id, to_user=request.user
            )
            if friend_request.status == const.REJECTED:

                payload = st.get_payload(
                    detail={},
                    message="Friend request already rejected.",
                    is_authenticated=st.is_authenticated_status(request),
                )
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)
            friend_request.status = const.REJECTED
            friend_request.save()

            payload = st.get_payload(
                detail={},
                message="Friend request rejected.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_200_OK)

        except FriendRequest.DoesNotExist:
            payload = st.get_payload(
                detail={},
                message="Friend request not found.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:

            payload = st.get_payload(
                detail={},
                message=f"{e}",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            payload = st.get_payload(
                detail={},
                message="An unexpected error occurred.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListFriendRequestsView(APIView):
    """
    View to handle listing friend requests based on their status.

    This view handles GET requests to list friend requests for the authenticated user.
    It filters the requests based on the status provided in the query parameters ('pending', 'accepted', 'rejected').
    Returns an appropriate response based on the status of the friend requests.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            request_status = request.query_params.get("status")

            if request_status == const.PENDING:
                requests_ = FriendRequest.objects.filter(
                    to_user=request.user, status=const.PENDING
                )

            elif request_status == const.ACCEPTED:
                requests_ = FriendRequest.objects.filter(
                    to_user=request.user, status=const.ACCEPTED
                )

            elif request_status == const.REJECTED:
                requests_ = FriendRequest.objects.filter(
                    to_user=request.user, status=const.REJECTED
                )
            else:
                payload = st.get_payload(
                    detail=[],
                    message="Invalid status",
                    is_authenticated=st.is_authenticated_status(request),
                )
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            serializer = FriendRequestSerializer(requests_, many=True)

            payload = st.get_payload(
                detail=serializer.data,
                message=f"{request_status} friend requests.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error: ", e)
            payload = st.get_payload(
                detail=[],
                message="An unexpected error occurred.",
                is_authenticated=st.is_authenticated_status(request),
            )
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ListFriendsAcceptedRequest(APIView):
    """
    View to list users who have accepted the current user's friend request.

    This view handles GET requests to retrieve users who have accepted the authenticated user's friend request.
    It queries the database to find users who have a status of 'accepted' in the friend request relationships.
    Returns the list of users who have accepted the friend request.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user

        # Users who have accepted the current user's friend request
        accepted_request_user_ = User.objects.filter(
            Q(sent_requests__to_user=user, sent_requests__status=const.ACCEPTED)
            | Q(
                received_requests__from_user=user,
                received_requests__status=const.ACCEPTED,
            )
        ).distinct()

        serialized_accepted_request_user = UserListSerializer(
            accepted_request_user_, many=True
        ).data

        payload = st.get_payload(
            detail=serialized_accepted_request_user,
            message="Users who have accepted the current user's friend request.",
            is_authenticated=st.is_authenticated_status(request),
        )
        return Response(data=payload, status=status.HTTP_200_OK)
