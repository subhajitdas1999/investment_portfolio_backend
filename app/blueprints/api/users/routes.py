from flask import jsonify, request
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import get_db_session # Import get_db_session from extensions
from app.__init__ import print_colored, Colors
from app.services.user_service import UserService
from app.models.user_model import User # Ensure correct model import path

# Import the blueprint object defined in this package's __init__.py
from . import users_bp

@users_bp.route('/', methods=['POST'])
def create_user():
    """
    Endpoint to create a new user (registration).
    Expects JSON: {"username": "...", "email": "...", "password_hash": "..."}
    """
    session = get_db_session()
    user_service = UserService(session)
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password_hash = data.get('password_hash')

        if not all([username, email, password_hash]):
            print_colored("Route: Missing required user fields for creation.", color=Colors.YELLOW)
            return jsonify(message="Missing required fields: username, email, password_hash."), 400

        new_user = user_service.create_user(username, email, password_hash)

        return jsonify(message="User created successfully!", user_id=new_user.id), 201
    except ValueError as ve:
        session.rollback()
        print_colored(f"Route: Validation error creating user: {ve}", color=Colors.YELLOW)
        return jsonify(message=str(ve)), 400
    except SQLAlchemyError as e:
        session.rollback()
        print_colored(f"Route: Database error creating user: {e}", color=Colors.RED, bold=True)
        return jsonify(message=f"Database error: {str(e)}", status="ERROR"), 500
    except Exception as e:
        session.rollback()
        print_colored(f"Route: An unexpected error occurred: {e}", color=Colors.RED, bold=True)
        return jsonify(message=f"An unexpected error occurred: {str(e)}", status="ERROR"), 500
    finally:
        session.close()

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Endpoint to retrieve a user by their ID.
    """
    session = get_db_session()
    user_service = UserService(session)
    try:
        user = user_service.get_user_by_id(user_id)

        return jsonify(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at.isoformat(),
            last_login_at=user.last_login_at.isoformat() if user.last_login_at else None
        ), 200
    except NoResultFound:
        print_colored(f"Route: User with ID: {user_id} not found.", color=Colors.YELLOW)
        return jsonify(message="User not found."), 404
    except SQLAlchemyError as e:
        print_colored(f"Route: Database error fetching user: {e}", color=Colors.RED, bold=True)
        return jsonify(message=f"Database error: {str(e)}", status="ERROR"), 500
    except Exception as e:
        print_colored(f"Route: An unexpected error occurred: {e}", color=Colors.RED, bold=True)
        return jsonify(message=f"An unexpected error occurred: {str(e)}", status="ERROR"), 500
    finally:
        session.close()