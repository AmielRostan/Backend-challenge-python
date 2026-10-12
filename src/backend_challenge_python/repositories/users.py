from sqlalchemy import select
from sqlalchemy.orm import Session

from backend_challenge_python.models.user import User


class UsersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all(self) -> list[User]:
        return list(self.db.scalars(select(User).order_by(User.id)).all())

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def update(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
