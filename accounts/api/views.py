from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from accounts.api.serializer import (
    SignUpSerializer,
    CustomTokenObtainPairSerializer,
    UserListSerializer,
)
from utils import st, StandardResultsSetPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class LoginAPIView(TokenObtainPairView):
    """
    API view for user login.

    This view handles the user login process by extending the TokenObtainPairView
    from Django REST framework's SimpleJWT package. It uses the CustomTokenObtainPairSerializer
    to validate the provided credentials and generate JWT tokens for authenticated users.
    """

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            payload = st.get_payload(
                detail=serializer.validated_data,
                message="User successfully loggedIn.",
                is_authenticated=True,
            )
            return Response(data=payload, status=status.HTTP_200_OK)

        else:
            payload = st.get_payload(
                detail={},
                message="Invalid Credentials",
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class SignUpAPIView(APIView):
    """
    API view for user sign-up.

    This view handles the user registration process. It uses the SignUpSerializer
    to validate and save the user data. If the data is valid, a new user is created.
    If there is an unexpected error during user creation, an appropriate error response is returned.
    """

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():

            try:
                serializer.save()
                payload = st.get_payload(
                    detail=serializer.data,
                    message="User created successfully.",
                    is_authenticated=True,
                )
                return Response(payload, status=status.HTTP_201_CREATED)

            except Exception as e:
                payload = st.get_payload(
                    detail={},
                    message=f"An un expected error Occurse: {e}",
                    is_authenticated=True,
                )
                return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(APIView):
    """
    API view for listing users.

    This view handles listing users with optional search functionality. It uses pagination
    to limit the number of users returned per request.
    """
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def __init__(self, **kwargs) -> None:
        self.userserializer = UserListSerializer
        self.pagination = StandardResultsSetPagination()
        self.user_qs = User.objects.all().order_by("-created_on")
        super().__init__(**kwargs)

    def search_users(self, queryset, search_keyword):
        """
        Filters the queryset based on the search keyword.
        If the keyword contains '@', it searches by email.
        Otherwise, it searches by name.
        """

        if search_keyword:
            if "@" in search_keyword:
                return queryset.filter(email__iexact=search_keyword)
            else:
                return queryset.filter(username__icontains=search_keyword)
        return queryset

    def get(self, request, *args, **kwargs):

        search_keyword = request.query_params.get("search", "")
        searched_user = self.search_users(
            queryset=self.user_qs, search_keyword=search_keyword
        )

        paginated_user_qs = self.pagination.paginate_queryset(searched_user, request)
        serialized_user_qs = self.userserializer(paginated_user_qs, many=True).data
        payload = st.get_payload(
            detail=serialized_user_qs,
            message="User list",
            is_authenticated=st.is_authenticated_status(request=request),
        )
        return Response(data=payload, status=status.HTTP_200_OK)
