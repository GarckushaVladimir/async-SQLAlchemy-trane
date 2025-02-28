from sqlalchemy import select

from dao.base import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User, Profile, Post, Comment


class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def add_user_with_profile(cls, session: AsyncSession, user_data: dict) -> User:
        """
        Добавляет пользователя и привязанный к нему профиль.

        Аргументы:
        - session: AsyncSession - асинхронная сессия базы данных
        - user_data: dict - словарь с данными пользователя и профиля

        Возвращает:
        - User - объект пользователя
        """

        user = cls.model(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        session.add(user)
        await session.flush()

        profile = Profile(
            user_id=user.id,
            first_name=user_data['first_name'],
            second_name=user_data.get('second_name'),
            age=user_data.get('age'),
            gender=user_data['gender'],
            profession=user_data.get('profession'),
            interests=user_data.get('interests'),
            contacts=user_data.get('contacts')
        )
        session.add(profile)

        await session.commit()

        return user

    @classmethod
    async def get_all_users(cls, session: AsyncSession):
        query = select(cls.model)

        result = await session.execute(query)

        records = result.scalars().all()

        return records

    @classmethod
    async def get_username_id(cls, session: AsyncSession):
        query = select(cls.model.id, cls.model.username)

        result = await session.execute(query)

        records = result.all()

        return records

    @classmethod
    async def update_username_age_by_id(cls, session: AsyncSession, data_id: int, username: str, age: int):
        user = await session.get(cls.model, data_id)
        user.username = username
        user.profile.age = age
        await session.flush()


class ProfileDAO(BaseDAO[Profile]):
    model = Profile


class PostDAO(BaseDAO[Post]):
    model = Post


class CommentDAO(BaseDAO[Comment]):
    model = Comment
