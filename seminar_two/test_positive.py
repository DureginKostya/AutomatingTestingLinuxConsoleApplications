import subprocess

TST = '/home/user/tst'
OUT = '/home/user/out'
FOLDER_E = '/home/user/folder_e'
FOLDER_X = '/home/user/folder_x'


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def get_hash_file(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if result.returncode == 0 and result.stdout != '':
        if ' crc32 ' in cmd:
            return result.stdout[:-1]
        out = result.stdout
        for elm in out.split('\n'):
            if 'CRC32  for data:' in elm:
                *_, sum_hash = elm.split()
                return sum_hash.lower()
    return None


def test_step1():
    # test1
    result1 = checkout(f'cd {TST}; 7z a {OUT}/arx2', 'Everything is Ok')
    result2 = checkout(f'cd {OUT}; ls', 'arx2.7z')
    assert result1 and result2, 'test1 FAIL'


def test_step2():
    # test2
    result1 = checkout(f'cd {OUT}; 7z e arx2.7z -o{FOLDER_E} -y', 'Everything is Ok')
    result2 = checkout(f'cd {FOLDER_E}; ls', 'folder_1')
    result3 = checkout(f'cd {FOLDER_E}; ls', 'folder_2')
    result4 = checkout(f'cd {FOLDER_E}; ls', 'folder_tst_file_1')
    result5 = checkout(f'cd {FOLDER_E}; ls', 'folder_tst_file_2')
    result6 = checkout(f'cd {FOLDER_E}; ls', 'folder_2_file_1')
    assert result1 and result2 and result3 and result4 and result5 and result6, 'test2 FAIL'


def test_step3():
    # test3
    result1 = checkout(f'cd {OUT}; 7z x arx2.7z -o{FOLDER_X} -y', 'Everything is Ok')
    result2 = checkout(f'cd {FOLDER_X}; ls', 'folder_1')
    result3 = checkout(f'cd {FOLDER_X}; ls', 'folder_tst_file_1')
    result4 = checkout(f'cd {FOLDER_X}; ls', 'folder_tst_file_2')
    result5 = checkout(f'cd {FOLDER_X}/folder_1; ls', 'folder_2')
    result6 = checkout(f'cd {FOLDER_X}/folder_1/folder_2; ls', 'folder_2_file_1')
    assert result1 and result2 and result3 and result4 and result5 and result6, 'test3 FAIL'


def test_step4():
    # test4
    assert checkout(f'cd {OUT}; 7z t arx2.7z', 'Everything is Ok'), 'test4 FAIL'


def test_step5():
    # test5
    result1 = checkout(f'cd {OUT}; 7z l arx2.7z', 'folder_1/folder_2/folder_2_file_1')
    result2 = checkout(f'cd {OUT}; 7z l arx2.7z', 'folder_tst_file_1')
    result3 = checkout(f'cd {OUT}; 7z l arx2.7z', 'folder_tst_file_2')
    result4 = checkout(f'cd {OUT}; 7z l arx2.7z', '3 files')
    result5 = checkout(f'cd {OUT}; 7z l arx2.7z', '2 folders')
    assert result1 and result2 and result3 and result4 and result5, 'test5 FAIL'


def test_step6():
    result_hash_7z_h = get_hash_file(f'cd {OUT}; 7z h arx2.7z')
    result_hash_crc32 = get_hash_file(f'cd {OUT}; crc32 arx2.7z')
    assert (result_hash_7z_h == result_hash_crc32 and
            result_hash_7z_h != None and
            result_hash_crc32 != None), 'test6 FAIL'


def test_step7():
    # test7
    assert checkout(f'cd {TST}; 7z u {OUT}/arx2.7z', 'Everything is Ok'), 'test7 FAIL'


def test_step8():
    # test8
    assert checkout(f'cd {OUT}; 7z d arx2.7z', 'Everything is Ok'), 'test8 FAIL'
