from django.urls import path
from friends.api.views import (
    SendFriendRequest,
    AcceptFriendRequestView,
    ListFriendRequestsView,
    RejectFriendRequestView,
    ListFriendsAcceptedRequest,
)

app_name = "friends"

urlpatterns = [
    path("send-request/api/v1", SendFriendRequest.as_view(), name="friend-request"),
    path(
        "accept-request/api/v1",
        AcceptFriendRequestView.as_view(),
        name="accept-request",
    ),
    path(
        "reject-request/api/v1",
        RejectFriendRequestView.as_view(),
        name="reject-request",
    ),
    path(
        "friend-requests/api/v1",
        ListFriendRequestsView.as_view(),
        name="list-friend-request",
    ),
    path(
        "freinds/accepted-request/api/v1",
        ListFriendsAcceptedRequest.as_view(),
        name="list-friends-accepted-request",
    ),
]
