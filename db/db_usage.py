from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import User, InputUrl, OutputUrl
from functional.url_to_short_url import generate_short_code


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

        # Генерируем код и проверяем его уникальность
        short_code = generate_short_code()
        result = await self.session.execute(
            select(OutputUrl)
            .where(OutputUrl.short_url == short_code)
        )
        # Если такой код уже есть – генерируем новый, пока не получим уникальный
        while result.scalar_one_or_none() is not None:
            short_code = generate_short_code()
            result = await self.session.execute(
                select(OutputUrl)
                .where(OutputUrl.short_url == short_code)
            )

        short_entry = OutputUrl(
            user_id=input_entry.user_id,
            input_url_id=input_entry.id,
            short_url=short_code # сохраняем только код, без домена
        )

        self.session.add(short_entry)
        await self.session.flush()
        await self.session.commit()

        return short_entry

    async def get_original_url(self, short_code: str) -> Optional[str]:
        """Find original URL with short code. Return original URL"""
        result = await self.session.execute(
            select(OutputUrl)
            .options(selectinload(OutputUrl.input_url))
            .where(OutputUrl.short_url == short_code)
        )
        output_entry = result.scalar_one_or_none()
        if output_entry and output_entry.input_url:
            return output_entry.input_url.text
        return None