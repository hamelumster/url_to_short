from datetime import datetime
from sqlalchemy import BigInteger, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    input_urls: Mapped[list["Url"]] = relationship(back_populates="user")

class InputUrl(Base):
    __tablename__ = "input_urls"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    user: Mapped["User"] = relationship(back_populates="input_urls")
    output_url: Mapped["OutputUrl"] = relationship(back_populates="input_url", uselist=False)

class OutputUrl(Base):
    __tablename__ = "output_urls"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    input_url_id: Mapped[int] = mapped_column(ForeignKey("input_urls.id"), unique=True)
    short_url: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    input_url: Mapped["InputUrl"] = relationship(back_populates="output_url")
