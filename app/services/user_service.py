from sqlalchemy.orm.session import Session as DBSessionType
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
# NEW: Import User from its modular location
from app.models.user_model import User
from app.__init__ import print_colored, Colors

class UserService:
    def __init__(self, db_session: DBSessionType):
        """
        Initializes the UserService with a database session.
        """
        self.session = db_session

    def create_user(self, username: str, email: str, password_hash: str) -> User:
        """
        Creates a new user in the database.
        Raises ValueError if user already exists (username or email).
        """
        # Basic validation (more comprehensive validation would be in a separate layer)
        if not username or not email or not password_hash:
            raise ValueError("Username, email, and password hash are required.")

        # Check if user already exists by username or email
        existing_user = self.session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            if existing_user.username == username:
                raise ValueError(f"User with username '{username}' already exists.")
            if existing_user.email == email:
                raise ValueError(f"User with email '{email}' already exists.")

        new_user = User(username=username, email=email, password_hash=password_hash)
        self.session.add(new_user)
        self.session.commit()
        print_colored(f"Service: User '{username}' created successfully with ID: {new_user.id}", color=Colors.GREEN)
        return new_user

    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieves a user by their ID.
        Raises NoResultFound if user does not exist.
        """
        user = self.session.query(User).filter_by(id=user_id).one()
        print_colored(f"Service: Retrieved user with ID: {user_id}", color=Colors.GREEN)
        return user