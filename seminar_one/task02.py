"""Задание 2:
Доработать функцию из предыдущего задания таким образом, чтобы у неё появился
дополнительный режим работы, в котором вывод разбивается на слова с удалением
всех знаков пунктуации (их можно взять из списка string.puctuation модуля
string). В этом режиме должно проверяться наличие слова в выводе."""

import subprocess
from string import punctuation


def find_info(command: str, search_condition: str, mode=0) -> bool:
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if result.returncode != 0:
        return False
    out = result.stdout
    if mode == 0:
        if search_condition in out:
            return True
    else:
        out = out.replace('\n', ' ')
        new_out = ''
        for ch in out:
            if ch in punctuation:
                new_out += ' '
            else:
                new_out += ch
        if search_condition in new_out.split():
            return True
    return False


if __name__ == '__main__':
    user_command = input('Введите команду: ')
    user_find = input('Введите условие поиска: ')
    user_mode = input('Режим поиска: <<по слову>>, [y/n]: ')
    if user_mode == 'y':
        print(find_info(user_command, user_find, 1))
    else:
        print(find_info(user_command, user_find))
