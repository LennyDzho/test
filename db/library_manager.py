import json
from typing import List, AsyncGenerator


class Book:
    def __init__(self, id: int, title: str, author: str, year: int, status: bool = True):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return (f'\nИнформация о книге:\n\n'
                f'ID книги: {self.id}\n'
                f'Название: {self.title}\n'
                f'Автор: {self.author}\n'
                f'Год издания: {self.year}\n'
                f'Статус: {"В наличии" if self.status else "Выдана"}\n'
                f'===================================================')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }


class LibraryManager:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.books: List[Book] = []

    async def load_books(self):
        try:
            with open(self.db_file, 'r', encoding='utf-8') as file:
                data = file.read()
                self.books = [Book(**book) for book in json.loads(data)]
        except FileNotFoundError:
            self.books = []

    async def save_books(self) -> None:
        with open(self.db_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps([book.to_dict() for book in self.books], ensure_ascii=False, indent=4))

    async def iteration_by_books(self) -> AsyncGenerator[Book, None]:
        for book in self.books:
            yield book

    async def add_book(self, title: str, author: str, year: int) -> str:
        new_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(id=new_id, title=title, author=author, year=year)
        self.books.append(new_book)
        await self.save_books()
        return f'\nКнига успешно добавлена:\n\n{new_book}'

    async def delete_book(self, book_id: int) -> str:
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                await self.save_books()
                return f'Книга с ID {book_id} успешно удалена.'
        return f'Книга с ID {book_id} не найдена.'

    async def search_books(self, book_id: int) -> str:
        for book in self.books:
            if book.id == book_id:
                return f'\nКнига найдена:\n\n{book}'
        return 'Книга не найдена.'

    async def change_status(self, book_id: int) -> str:
        for book in self.books:
            if book.id == book_id:
                book.status = not book.status
                await self.save_books()
                return (f'\nСтатус книги с ID {book.id} изменён.\n'
                        f'Новый статус: {"В наличии" if book.status else "Выдана"}')
        return 'Книга не найдена.'

    async def get_all_books(self) -> str:
        message = ''
        async for book in self.iteration_by_books():
            message += str(book) + '\n'
        return message
