from sqlalchemy import ARRAY, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend_challenge_python.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    pokemon_ids: Mapped[list[int]] = mapped_column(
        ARRAY(Integer),
        default=list,
    )
