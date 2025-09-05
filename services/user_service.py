from typing import cast

from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from db.models.users import User


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def add_user(
        self, username: str, password: str, email: str, role: str = "user"
    ) -> User:
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            email=email,
            role=role,
        )
        self.session.add(user)
        self.session.commit()
        return user

    def update_user(
        self,
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        role: str | None = None,
    ):
        user: User = self.session.get(User, user_id)
        if not user:
            return
        if username is not None:
            user.username = username
        if password is not None:
            user.password_hash = generate_password_hash(password)
        if email is not None:
            user.email = email
        if role is not None:
            user.role = role
        self.session.commit()

    def delete_users(self, user_ids: list[int]):
        for uid in user_ids:
            user = self.session.get(User, uid)
            if user:
                self.session.delete(user)
        self.session.commit()

    def get_all_users(self) -> list[User]:
        return cast(list[User], self.session.query(User).all())
