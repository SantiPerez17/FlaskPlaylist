from functools import wraps
import jwt
from flask import request, abort, current_app
from playlist.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get the token from the Authorization header
        token = request.headers.get("Authorization", "").split(" ")[1]
        if not token:
            # Abort with 401 Unauthorized if token is missing
            abort(401, description="Authentication Token is missing!")

        try:
            # Decode the token using the SECRET_KEY
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            # Get the current user based on the decoded email from the token
            current_user = User.query.filter_by(email=data['email']).first()
            if current_user is None:
                # Abort with 401 Unauthorized if the user is not found
                abort(401, description="Invalid Authentication token!")
        except jwt.DecodeError as e:
            # Abort with 401 Unauthorized if there's a decoding error
            abort(401, description=str(e))
        except Exception as e:
            # Abort with 500 Internal Server Error for other exceptions
            abort(500, description="Something went wrong")

        # Call the decorated function with the current user and other arguments
        return f(current_user, *args, **kwargs)

    return decorated
