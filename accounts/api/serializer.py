from rest_framework import serializers
from accounts.models import User
from utils import Settings as st
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from datetime import datetime


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining JWT tokens using email and password.

    This serializer extends the TokenObtainPairSerializer to authenticate users using their
    email and password. It validates the email format and ensures the credentials are correct.
    If the credentials are valid, it returns access and refresh tokens.

    -----------
    Attributes:
        email (serializers.CharField): The email field for user authentication.
        password (serializers.CharField): The password field for user authentication.
    """

    email = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self, value):
        """
        Validates the email format and ensures it adheres to the specified criteria.

        ----
        Args:
            value (str): The email address to be validated.

        ------
        Raises:
            serializers.ValidationError: If the email is invalid.

        -------
        Returns:
            str: The validated email in lowercase.
        """

        is_valid = st.email_validate(email=value.lower())
        if not is_valid:
            raise serializers.ValidationError(detail="Invalid Email...!")
        return value

    def validate(self, attrs):
        """
        Authenticates the user using the provided email and password.

        Converts the email to lowercase and attempts to authenticate the user.
        If the credentials are valid, generates and returns JWT tokens.

        -----
        Args:
            attrs (dict): The dictionary containing email and password.

        -------
        Raises:
            serializers.ValidationError: If the credentials are invalid.

        -------
        Returns:
            dict: A dictionary containing the access and refresh tokens.
        """

        credentials = {
            "email": attrs.get("email").lower(),
            "password": attrs.get("password"),
        }
        user = authenticate(**credentials)

        if user is None:
            raise serializers.ValidationError(
                detail={"message": "Invalid Credentials."}
            )

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class SignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for user sign-up.

    This serializer handles the creation of new users by ensuring that the necessary
    fields are provided and valid. It also verifies that the password and confirm_password
    fields match and that the email is in the correct format.

    ----------
    Attributes:
        confirm_password (serializers.CharField): The field for confirming the user's password.

    ----
    Meta:
        model (User): The User model to be used.
        fields (list): The list of fields to be included in the serialized data.
        extra_fields (dict): Additional field attributes, specifying required fields.
    """

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
        extra_fields = {
            "email": {"required": True},
            "password": {"required": True},
        }

    def create(self, validated_data):
        """
        Creates a new user with the provided validated data.

        -----
        Args:
            validated_data (dict): The validated data from the serializer.

        -------
        Returns:
            User: The created user object.
        """

        validated_data.pop("confirm_password")
        email = self.validated_data.get("email").lower()
        password = self.validated_data.get("password")
        username = self.validated_data.get("username")
        return User.objects.create_user(
            email=email, password=password, username=username
        )

    def validate_email(self, value):
        """
        Validates the email format and ensures it adheres to the specified criteria.

        -----
        Args:
            value (str): The email address to be validated.

        ------
        Raises:
            serializers.ValidationError: If the email is invalid.

        -------
        Returns:
            str: The validated email in lowercase.
        """

        is_valid = st.email_validate(email=value.lower())
        if not is_valid:
            raise serializers.ValidationError("Invalid Email...!")
        return value

    def validate(self, data):
        """
        Validates that the password and confirm_password fields match.

        ----
        Args:
            data (dict): The data to be validated.

        ------
        Raises:
            serializers.ValidationError: If the passwords do not match.

        --------
        Returns:
            dict: The validated data.
        """
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing user details.

    This serializer handles the conversion of User model instances into JSON
    format for API responses. It includes additional fields for formatting dates
    of birth, creation, and update times.

    Attributes:
        dob (serializers.SerializerMethodField): A formatted date of birth.
        created_on (serializers.SerializerMethodField): A formatted creation date and time.
        updated_on (serializers.SerializerMethodField): A formatted update date and time.

    Meta:
        model (User): The User model to be used.
        fields (list): The list of fields to be included in the serialized data.
    """

    dob = serializers.SerializerMethodField()
    created_on = serializers.SerializerMethodField()
    updated_on = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "mobile_no",
            "gender",
            "nationality",
            "dob",
            "created_on",
            "updated_on",
            "current_city",
            "slug",
        ]

    def get_updated_on(self, obj=None):
        """
        Formats the updated_on field of the User model.

        Args:
            obj (User): The User instance.

        Returns:
            str: The formatted updated_on date and time, or None if obj is None.
        """

        if obj:
            return datetime.strftime(obj.updated_on, "%d %b, %Y %H:%M:%S")
        return None

    def get_created_on(self, obj=None):
        """
        Formats the created_on field of the User model.

        Args:
            obj (User): The User instance.

        Returns:
            str: The formatted created_on date and time, or None if obj is None.
        """

        if obj:
            return datetime.strftime(obj.created_on, "%d %b, %Y, %H:%M:%S")
        return None

    def get_dob(self, obj=None):
        """
        Formats the dob field of the User model.

        Args:
            obj (User): The User instance.

        Returns:
            str: The formatted dob date and time, or None if obj is None.
        """
        if obj:
            return datetime.strftime(obj.created_on, "%d %b, %Y, %H:%M:%S")
        return None
