import os
import sys

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    punctuation_symbols = ',.!:;?'
    page_text = text[start:start + size]

    index = len(page_text)
    while (page_text[index - 1] not in punctuation_symbols
           or text[index] in punctuation_symbols
           or page_text[index - 2] in punctuation_symbols):
        index -= 1
    return page_text[:index], len(page_text[:index])


# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as book_file:
        text = book_file.read()

    start, page_number = 0, 1
    while start < len(text):
        page_text, page_size = _get_part_text(text, start, PAGE_SIZE)
        book[page_number] = page_text.lstrip()
        start += page_size
        page_number += 1


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))

