from rest_framework_simplejwt.tokens import RefreshToken


def token_for_user_as_login(user) -> dict:
    """
        This function creates access and refresh tokens for a user and returns us them as a dictionary.
    """
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
