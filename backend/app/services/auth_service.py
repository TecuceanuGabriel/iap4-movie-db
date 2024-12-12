import jwt
import datetime

from app.config import Config


def generate_token(email):
    """Generate a JWT token with the given email as the payload.

    Parameters:
        email (str): The email to include in the payload.

    Returns:
        str: The generated token.
    """

    return jwt.encode(
        {
            "email": email,
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
        },
        Config.JWT_SECRET,
        algorithm="HS256",
    )


def verify_token(token):
    """Verify a JWT token and return the payload or an error message if needed.

    Parameters:
        token (str): The token to verify.

    Returns:
        tuple: token payload or None, error message or None
    """

    try:
        return (
            jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"]),
            None,
        )
    except jwt.ExpiredSignatureError:
        return None, {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return None, {"error": "Invalid token"}
