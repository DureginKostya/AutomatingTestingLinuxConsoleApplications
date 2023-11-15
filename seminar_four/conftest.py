import string
import pytest
import yaml
from ssh_checkers import ssh_checkout
from files import upload_files, ssh_getout
from random import choices
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope='module')
def clear_folders():
    return ssh_checkout(f'{data["ip"]}',
                        f'{data["user"]}',
                        f'{data["passwd"]}',
                        f'rm -rf {data["TST"]}/* {data["OUT"]}/* {data["FOLDER_E"]}/* {data["FOLDER_X"]}/*',
                        '')


@pytest.fixture(autouse=True, scope='module')
def deploy():
    res = []
    upload_files(f'{data["ip"]}',
                 f'{data["user"]}',
                 f'{data["passwd"]}',
                 '/home/user/p7zip-full.deb',
                 '/home/user2/p7zip-full.deb')
    upload_files(f'{data["ip"]}',
                 f'{data["user"]}',
                 f'{data["passwd"]}',
                 '/home/user/libarchive-zip-perl.deb',
                 '/home/user2/libarchive-zip-perl.deb')
    res.append(ssh_checkout(f'{data["ip"]}',
                            f'{data["user"]}',
                            f'{data["passwd"]}',
                            'echo "2222" | sudo -S dpkg -i /home/user2/p7zip-full.deb',
                            'Настраивается пакет'))
    res.append(ssh_checkout(f'{data["ip"]}',
                            f'{data["user"]}',
                            f'{data["passwd"]}',
                            'echo "2222" | sudo -S dpkg -s p7zip-full',
                            'Status: install ok installed'))
    res.append(ssh_checkout(f'{data["ip"]}',
                            f'{data["user"]}',
                            f'{data["passwd"]}',
                            'echo "2222" | sudo -S dpkg -i /home/user2/libarchive-zip-perl.deb',
                            'Настраивается пакет'))
    res.append(ssh_checkout(f'{data["ip"]}',
                            f'{data["user"]}',
                            f'{data["passwd"]}',
                            'echo "2222" | sudo -S dpkg -s libarchive-zip-perl',
                            'Status: install ok installed'))
    return all(res)


@pytest.fixture()
def make_bad_arx():
    ssh_checkout(f'{data["ip"]}',
                 f'{data["user"]}',
                 f'{data["passwd"]}',
                 f'cd {data["TST"]}; 7z a {data["OUT"]}/bad_arx -t{data["type"]}',
                 'Everything is Ok')
    ssh_checkout(f'{data["ip"]}',
                 f'{data["user"]}',
                 f'{data["passwd"]}',
                 f'truncate -s 1 {data["OUT"]}/bad_arx.{data["type"]}',
                 '')


@pytest.fixture(autouse=True, scope='class')
def make_files(make_folders):
    start_value = 0
    end_value = data['count'] - 1
    for key in make_folders.keys():
        for _ in range(start_value, end_value):
            file_name = ''.join(choices(string.ascii_uppercase + string.digits, k=5))
            if ssh_checkout(f'{data["ip"]}',
                            f'{data["user"]}',
                            f'{data["passwd"]}',
                            f'cd {key}; '
                            f'dd if=/dev/urandom of={file_name} bs={data["bs"]} count=1 iflag=fullblock',
                            ''):
                make_folders[key].append(file_name)
        start_value = end_value
        end_value = data['count']
    return make_folders


@pytest.fixture(autouse=True, scope='module')
def make_folders():
    ssh_checkout(f'{data["ip"]}',
                 f'{data["user"]}',
                 f'{data["passwd"]}',
                 f'mkdir -p {data["TST"]} {data["OUT"]} {data["FOLDER_E"]} {data["FOLDER_X"]}',
                 '')
    dict_folders = {f'{data["TST"]}': []}
    folder_name = 'folder_' + ''.join(choices(string.ascii_uppercase + string.digits, k=3))
    if ssh_checkout(f'{data["ip"]}',
                    f'{data["user"]}',
                    f'{data["passwd"]}',
                    f'mkdir {data["TST"]}/{folder_name}',
                    ''):
        dict_folders[f'{data["TST"]}/{folder_name}'] = []
    return dict_folders


@pytest.fixture(autouse=True)
def safe_log():
    yield
    last_line = ssh_getout(f'{data["ip"]}',
                           f'{data["user"]}',
                           f'{data["passwd"]}',
                           f'cat cd {data["stat_processes"]} | tail -n1')
    with open(f'{data["file_name_stat"]}', 'a', encoding='utf-8') as file_stat:
        file_stat.write(f'{datetime.now().strftime("%H:%M:%S:%f")} | '
                        f'{data["count"]} | '
                        f'{data["bs"]} | '
                        f'{last_line}')


@pytest.fixture(autouse=True, scope='session')
def start_and_end_execute():
    with open(f'{data["file_name_stat"]}', 'w'):
        pass
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    yield
    with open(f'{data["file_name_stat"]}', 'a', encoding='utf-8') as file_stat:
        file_stat.write(ssh_getout(f'{data["ip"]}',
                                   f'{data["user"]}',
                                   f'{data["passwd"]}',
                                   f"journalctl --since '{today}'"))
