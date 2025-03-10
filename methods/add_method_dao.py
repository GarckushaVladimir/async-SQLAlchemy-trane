from typing import List

from dao.dao import UserDAO
from dao.database import connection
from sqlalchemy.ext.asyncio import AsyncSession


@connection
async def add_one(user_data: dict, session: AsyncSession):
    new_user = await UserDAO.add(session=session, **user_data)
    print(f"Добавлен новый пользователь с ID: {new_user.id}")
    return new_user.id


# run(add_one(user_data={"username": "oliver_jackson", "email": "oliver.jackson@example.com", "password": "jackson123"}))

@connection
async def add_many_users(users_data: List[dict], session: AsyncSession):
    new_users = await UserDAO.add_many(session=session, instances=users_data)
    user_ids_list = [user.id for user in new_users]
    print(f"Добавлены новые пользователи с ID: {user_ids_list}")
    return user_ids_list


# users = [
#     {"username": "amelia_davis", "email": "amelia.davis@example.com", "password": "davispassword"},
#     {"username": "lucas_white", "email": "lucas.white@example.com", "password": "whiteSecure"},
#     {"username": "mia_moore", "email": "mia.moore@example.com", "password": "moorepass098"},
#     {"username": "benjamin_hall", "email": "benjamin.hall@example.com", "password": "hallben123"},
#     {"username": "sophia_hill", "email": "sophia.hill@example.com", "password": "hillSophia999"},
#     {"username": "liam_green", "email": "liam.green@example.com", "password": "greenSecure789"},
#     {"username": "isabella_clark", "email": "isabella.clark@example.com", "password": "clarkIsabella001"},
#     {"username": "ethan_baker", "email": "ethan.baker@example.com", "password": "bakerEthan555"},
#     {"username": "charlotte_scott", "email": "charlotte.scott@example.com", "password": "scottcharl333"},
#     {"username": "logan_young", "email": "logan.young@example.com", "password": "younglogan876"}
# ]
# run(add_many_users(users_data=users))

@connection
async def add_full_user(user_data: dict, session: AsyncSession):
    new_user = await UserDAO.add_user_with_profile(session=session, user_data=user_data)
    print(f"Добавлен новый пользователь с ID: {new_user.id}")
    return new_user.id

# user_data_bob = {
#     "username": "bob_smith1",
#     "email": "bob.smith1@example.com",
#     "password": "bobsecure456",
#     "first_name": "Bob",
#     "second_name": "Smith",
#     "age": 25,
#     "gender": GenderEnum.MALE,
#     "profession": ProfessionsEnum.DESIGNER,
#     "interests": ["gaming", "photography", "traveling"],
#     "contacts": {"phone": "+987654321", "email": "bob.smith@example.com"}
# }
# run(add_full_user(user_data=user_data_bob))
