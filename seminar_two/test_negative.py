import subprocess

OUT = '/home/user/out'
FOLDER_E = '/home/user/folder_e'


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False


def test_step1():
    # test1
    assert checkout(f'cd {OUT}; 7z e bad_arx.7z -o{FOLDER_E} -y', 'ERRORS'), 'test1 FAIL'


def test_step2():
    # test2
    assert checkout(f'cd {OUT}; 7z t bad_arx.7z', 'ERRORS'), 'test2 FAIL'
