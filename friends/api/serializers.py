from rest_framework import serializers
from friends.models import FriendRequest
from django.utils import timezone
from datetime import timedelta


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the FriendRequest model.

    This serializer serializes all fields of the FriendRequest model and includes additional
    methods to get the from_user and to_user fields as a string representation containing
    the user's email and ID.
    """

    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = "__all__"

    def get_from_user(self, obj):
        """
        Returns the from_user email and ID.

        ----
        Args:
            obj (FriendRequest): The FriendRequest instance.

        --------
        Returns:
            str: The email and ID of the from_user.
        """
        if obj:
            return f"{obj.from_user.email}, {obj.from_user.id}"
        raise serializers.ValidationError(
            detail={"message": "From user can not be None."}
        )

    def get_to_user(self, obj):
        """
        Returns the to_user email and ID.

        -----
        Args:
            obj (FriendRequest): The FriendRequest instance.

        -------
        Returns:
            str: The email and ID of the to_user.
        """

        if obj:
            return f"{obj.to_user.email}, {obj.to_user.id}"
        raise serializers.ValidationError(
            detail={"message": "Send to friend can not be None."}
        )


class SendFrientRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for sending a friend request.

    This serializer validates and creates FriendRequest instances. It includes validation
    methods to ensure that the request is not sent to oneself, that the request hasn't been
    sent already, and that the user does not exceed the limit of sending three requests per minute.
    """

    class Meta:
        model = FriendRequest
        fields = ["to_user"]

    def validate_to_user(self, value):
        """
        Validates the to_user field.
        Ensures that the sender is not trying to send a friend request to themselves.
        """

        if value is None:
            if value is None:
                raise serializers.ValidationError("Bad Request")

        elif value.id == self.context["request"].user.id:
            raise serializers.ValidationError(
                "You cannot send a friend request to yourself."
            )
        return value

    def validate(self, attrs):
        """
        Validates the attributes of the friend request.

        Checks if the user has already sent a friend request to the target user and ensures that the user does not
        exceed the limit of sending three requests per minute.
        """
        from_user = self.context["request"].user
        to_user = attrs.get("to_user")

        now = timezone.now()
        one_minute_ago = now - timedelta(minutes=1)

        # Check if the user has already sent a friend request to the target user
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise serializers.ValidationError("Friend request already sent.")

        # # Check the number of requests sent in the last minute
        recent_requests_count = FriendRequest.objects.filter(
            from_user=from_user, created_at__gte=one_minute_ago
        ).count()

        if recent_requests_count >= 3:
            raise serializers.ValidationError(
                "You can only send 3 friend requests per minute."
            )
        return attrs

    def create(self, validated_data):
        """
        Creates a FriendRequest instance with the validated data.
        """
        from_user = self.context["request"].user
        return FriendRequest.objects.create(
            from_user=from_user, to_user=validated_data["to_user"], status="pending"
        )
