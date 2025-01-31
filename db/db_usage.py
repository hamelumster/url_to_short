from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, InputUrl, OutputUrl
from functional.url_to_short_url import url_to_short_url


class DatabaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(self, user_id: int, username: str) -> User:
        """Create user and write data to DB"""
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            user = User(id=user_id, username=username)
            self.session.add(user)
            await self.session.flush()  # Используем flush вместо commit
        return user

    async def save_input_text(self, user_id: int, text: str) -> InputUrl:
        """Save any text from user input"""
        print(f"Сохраняем ввод: {text}")

        input_entry = InputUrl(user_id=user_id, text=text)
        self.session.add(input_entry)
        await self.session.flush()
        await self.session.commit()

        return input_entry

    async def generate_short_url(self, input_entry: InputUrl) -> OutputUrl:
        """Create short url and save data to DB"""
        if not input_entry.text.startswith("http"):
            print("❌ Введённый текст не является ссылкой, короткая не создаётся.")
            return None

        short_code = url_to_short_url(input_entry.text)
        short_entry = OutputUrl(user_id=input_entry.user_id, input_url_id=input_entry.id, short_url=short_code)

        self.session.add(short_entry)
        await self.session.flush()
        await self.session.commit()

        return short_entry