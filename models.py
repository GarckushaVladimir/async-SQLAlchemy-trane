from sqlalchemy import ForeignKey, text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, uniq_str, array_or_none, content_an

from sql_enums import GenderEnum, ProfessionsEnum, StatusPost, RatingEnum


class User(Base):
    username: Mapped[uniq_str]
    email: Mapped[uniq_str]
    password: Mapped[str]
    profile_id: Mapped[int | None] = mapped_column(ForeignKey('profiles.id'))

    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        lazy="joined"
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Profile(Base):
    first_name: Mapped[str]
    second_name: Mapped[str | None]
    age: Mapped[int | None]
    gender: Mapped[GenderEnum]
    profession: Mapped[ProfessionsEnum] = mapped_column(
        default=ProfessionsEnum.DEVELOPER,
        server_default=text("'UNEMPLOYED'")
    )
    interests: Mapped[array_or_none]
    contacts: Mapped[dict | None] = mapped_column(JSON)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
        uselist=False
    )


class Post(Base):
    title: Mapped[str]
    content: Mapped[content_an]
    main_photo_url: Mapped[str]
    photos_url: Mapped[array_or_none]
    status: Mapped[StatusPost] = mapped_column(
        default=StatusPost.PUBLISHED,
        server_default=text("'DRAFT'")
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )


class Comment(Base):
    content: Mapped[content_an]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    is_published: Mapped[bool] = mapped_column(
        default=True,
        server_default=text("'false'")
    )
    rating: Mapped[RatingEnum] = mapped_column(
        default=RatingEnum.FIVE,
        server_default=text("'SEVEN'")
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="comments"
    )

    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments"
    )
