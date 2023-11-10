import string
import pytest
import yaml
from datetime import datetime
from checkers import checkout, get_last_line_file
from random import choices

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope='session')
def make_folders():
    return checkout(f'mkdir -p {data["TST"]} '
                    f'{data["OUT"]} '
                    f'{data["FOLDER_E"]} '
                    f'{data["FOLDER_X"]}',
                    '')


@pytest.fixture(autouse=True, scope='class')
def make_files():
    list_off_files = []
    for i in range(data["count"]):
        filename = ''.join(choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(f'cd {data["TST"]}; dd if=/dev/urandom of={filename} '
                    f'bs={data["bs"]} count=1 iflag=fullblock',
                    ''):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture(autouse=True, scope='session')
def clear_folders():
    return checkout(f'rm -rf {data["TST"]}/* '
                    f'{data["OUT"]}/* '
                    f'{data["FOLDER_E"]}/* '
                    f'{data["FOLDER_X"]}/*',
                    '')


@pytest.fixture()
def make_bad_arx():
    checkout(f'cd {data["TST"]}; 7z a {data["OUT"]}/bad_arx -t{data["type"]}',
             'Everything is Ok')
    checkout(f'truncate -s 1 {data["OUT"]}/bad_arx.{data["type"]}',
             '')


@pytest.fixture(autouse=True, scope='session')
def create_file_stat():
    checkout(f'cd {data["OUT"]}; cat > {data["file_name_stat"]}', '')


@pytest.fixture(autouse=True)
def write_info_to_file_stat():
    yield
    last_line = get_last_line_file(f'{data["stat_processes"]}')
    with open(f'{data["OUT"]}/{data["file_name_stat"]}', 'a', encoding='utf-8') as file_stat:
        file_stat.write(f'{datetime.now().strftime("%H:%M:%S:%f")} | '
                        f'{data["count"]} | '
                        f'{data["bs"]} | '
                        f'{last_line}\n')
