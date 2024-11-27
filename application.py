import asyncio
import os

from db.library_manager import LibraryManager


class App:
    def __init__(self):
        print(f"=====================================")
        print(f"=========== CONFIGURATION ===========")
        print(f"=====================================")
        self.library_manager = LibraryManager(os.path.join(os.getcwd(), 'db', 'library.json'))
        self.actions = {
            '1': self.add_book,
            '2': self.delete_book,
            '3': self.search_book,
            '4': self.change_status,
            '5': self.view_all_books,
            '6': self.exit_app
        }

    async def __call__(self):
        await self.library_manager.load_books()
        await self.start()
        return 'Заходи ещё!'

    async def start(self):
        while True:
            print(f'\nВыберите действие: \n'
                  f'1 - Добавить книгу\n'
                  f'2 - Удалить книгу\n'
                  f'3 - Найти книгу\n'
                  f'4 - Изменить статус книги\n'
                  f'5 - Показать все книги\n'
                  f'6 - Выйти\n')
            choice = input('Введите номер действия: ')
            action = self.actions.get(choice)
            if action:
                await action()
            else:
                print('Некорректный выбор, попробуйте снова.')

    def get_input(self, prompt: str, data_type=str, allowed_range=None) -> str:
        while True:
            user_input = input(f'{prompt} (или введите "выйти" для возврата в меню): ')
            if user_input.lower() == 'выйти':
                return 'выйти'

            try:
                value = data_type(user_input)
                if allowed_range and (value < allowed_range[0] or value > allowed_range[1]):
                    print(f'Введите значение в диапазоне от {allowed_range[0]} до {allowed_range[1]}.')
                    continue
                return value
            except ValueError:
                print(f'Введите корректное значение типа {data_type.__name__}.')

    async def add_book(self):
        title = self.get_input('Введите название книги:')
        if title == 'выйти':
            return
        author = self.get_input('Введите автора книги:')
        if author == 'выйти':
            return
        year = self.get_input('Введите год издания:', data_type=int, allowed_range=(0, 2024))
        if year == 'выйти':
            return

        result = await self.library_manager.add_book(title, author, year)
        print(result)

    async def delete_book(self):
        book_id = self.get_input('Введите ID книги для удаления:', data_type=int)
        if book_id == 'выйти':
            return

        result = await self.library_manager.delete_book(book_id)
        print(result)

    async def search_book(self):
        book_id = self.get_input('Введите ID книги для поиска:', data_type=int)
        if book_id == 'выйти':
            return

        result = await self.library_manager.search_books(book_id)
        print(result)

    async def change_status(self):
        book_id = self.get_input('Введите ID книги для изменения статуса:', data_type=int)
        if book_id == 'выйти':
            return

        result = await self.library_manager.change_status(book_id)
        print(result)

    async def view_all_books(self):
        result = await self.library_manager.get_all_books()
        print(result)

    async def exit_app(self):
        print('Завершение работы...')
        exit()


if __name__ == '__main__':
    app = App()
    asyncio.run(app())
