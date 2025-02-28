from asyncio import run

from pydantic import create_model, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from dao.dao import UserDAO
from dao.session_maker import connection

from schemas import UserPydantic


@connection(commit=False)
async def select_all_users(session: AsyncSession):
    return await UserDAO.get_all_users(session)


# all_users = run(select_all_users())
# for i in all_users:
#     user_pydantic = UserPydantic.from_orm(i)
#     print(user_pydantic.dict())

@connection(commit=False)
async def select_username_id(session: AsyncSession):
    return await UserDAO.get_username_id(session)


# rez = run(select_username_id())
# for i in rez:
#     rez = UsernameIdPydantic.from_orm(i)
#     print(rez.dict())

@connection(commit=False)
async def select_full_user_info(session: AsyncSession, user_id: int):
    user = await UserDAO.find_one_or_none_by_id(session=session, data_id=user_id)
    if user:
        return UserPydantic.model_validate(user).model_dump()
    return {"message": f'Пользователь с ID {user_id} не найден!'}


# info = run(select_full_user_info(user_id=8))
# print(info)

@connection(commit=False)
async def select_full_user_info_email(session: AsyncSession, user_id: int, email: str):
    FilterModel = create_model(
        'FilterModel',
        id=(int, ...),
        email=(EmailStr, ...)
    )

    user = await UserDAO.find_one_or_none(session=session, filters=FilterModel(id=user_id, email=email))

    if user:
        # Преобразуем ORM-модель в Pydantic-модель и затем в словарь
        return UserPydantic.model_validate(user).model_dump()

    return {"message": f'Пользователь с ID {user_id} не найден!'}

# info = run(select_full_user_info_email(user_id=9, email='john.doe12@example.com'))
# print(info)
