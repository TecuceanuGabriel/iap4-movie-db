import jwt
import datetime

from app.config import Config

def generate_token(email):
    return jwt.encode(
        {
            "email": email,
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
        },
        Config.JWT_SECRET,
        algorithm="HS256",
    )


def verify_token(token):
    try:
        return (
            jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"]),
            None,
        )
    except jwt.ExpiredSignatureError:
        return None, {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return None, {"error": "Invalid token"}
