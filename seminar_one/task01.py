"""Задание 1:
Написать функцию на Python, которой передаются в качестве параметров
команда и текст. Функция должна возвращать True, если команда успешно
выполнена и текст найден в её выводе и False в противном случае.
Передаваться должна только одна строка, разбиение вывода использовать
не нужно."""

import subprocess


def find_info(command: str, search_condition: str) -> bool:
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if result.returncode != 0:
        return False
    if search_condition in result.stdout:
        return True
    return False


if __name__ == '__main__':
    user_command = input('Введите команду: ')
    user_find = input('Введите условие поиска: ')
    print(find_info(user_command, user_find))
