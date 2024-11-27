### Бибилиотечная система
Данная система имеет всего 3 класса:
- 'Book' - описывает структуру хранения книжки в json файле
- 'LibraryManager' - можно описать как 
- app - класс самого приложения, где описаны методы для его радоты

---

### Методы классов

##### `Класс Book`

`__init__(self, id: int, title: str, author: str, year: int, status: bool = True)`
- Инициализирует объект книги с уникальным ID, названием, автором, годом издания и статусом (по умолчанию "В наличии").

`__str__(self)`
- Возвращает строковое представление объекта книги с информацией о книге.

`to_dict(self)`
- Преобразует объект книги в словарь для сохранения в JSON-файле.

---

##### `Класс LibraryManager`

`__init__(self, db_file: str)`
- Инициализирует менеджер библиотеки с указанием пути к файлу JSON, в котором будут храниться данные о книгах.

`load_books(self)`
- Загружает данные о книгах из JSON-файла и создает объекты книг.

`save_books(self) -> None`
- Сохраняет текущий список книг в JSON-файл.

`iteration_by_books(self) -> Generator[Book, None, None]`
- Возвращает генератор для итерации по всем книгам в библиотеке.

`add_book(self, title: str, author: str, year: int) -> str`
- Добавляет новую книгу в библиотеку с указанными названием, автором и годом издания. Присваивает книге уникальный ID и сохраняет изменения в JSON-файле.

`delete_book(self, book_id: int) -> str`
- Удаляет книгу с указанным ID из библиотеки, если она существует, и сохраняет изменения в JSON-файле.

`search_books(self, book_id: int) -> str`
`Ищет книгу по её ID и возвращает информацию о книге, если она найдена.`

`change_status(self, book_id: int) -> str`
- Изменяет статус книги с указанным ID на "В наличии" или "Выдана" и сохраняет изменения в JSON-файле.

`get_all_books(self) -> str`
- Возвращает информацию о всех книгах в библиотеке в виде строки

---
Тут я пытался попробовать отсимулировать работу сервера, на стороне которого обрабатываются те или иные данные.
Соответственно без ассинхронности тут не обойтись. Однако файлики ассинхронно открыть без стороннего модуля не получится, поэтому методы `load_books` и `save_books` из класса `LibraryManager` должны были бы выглядеть так:

```python
import aiofiles

class LibraryManager:
    ...
    async def load_books(self):
        try:
            async with aiofiles.open(self.db_file, 'r', encoding='utf-8') as file:
                data = await file.read()
                self.books = [Book(**book) for book in json.loads(data)]
        except FileNotFoundError:
            self.books = []

    async def save_books(self) -> None:
        async with aiofiles.open(self.db_file, 'w', encoding='utf-8') as file:
            await file.write(json.dumps([book.to_dict() for book in self.books], ensure_ascii=False, indent=4))
    ...
```

---

### Зависимости
- Программа использует только стандартные библиотеки Python (такие как json и typing). Нет сторонних зависимостей.

**Примечание**
- Все данные сохраняются в JSON-файле library.json, который должен находиться в одной папке с library_manager.py, если не указано иное.

---

### Установка и запуск
- Склонируйте репозиторий.
- Перейдите в директорию проекта.
- Запустите файл main.py для начала работы с библиотекой.

```bash
python main.py
```
