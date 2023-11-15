import yaml
from ssh_checkers import ssh_checkout
from files import ssh_getout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_step1(self):
        # test1
        result1 = ssh_checkout(f'{data["ip"]}',
                               f'{data["user"]}',
                               f'{data["passwd"]}',
                               f'cd {data["TST"]}; 7z a {data["OUT"]}/arx2 -t{data["type"]}',
                               'Everything is Ok')
        result2 = ssh_checkout(f'{data["ip"]}',
                               f'{data["user"]}',
                               f'{data["passwd"]}',
                               f'cd {data["OUT"]}; ls',
                               f'arx2.{data["type"]}')
        assert result1 and result2, 'test1 FAIL'

    def test_step2(self, make_files):
        # test2
        res = [ssh_checkout(f'{data["ip"]}',
                            f'{data["user"]}',
                            f'{data["passwd"]}',
                            f'cd {data["OUT"]}; 7z e arx2.{data["type"]} -o{data["FOLDER_E"]} -y',
                            'Everything is Ok')]
        for key, value in make_files.items():
            if key != data['TST']:
                *_, folder = key.split('/')
                res.append(ssh_checkout(f'{data["ip"]}',
                                        f'{data["user"]}',
                                        f'{data["passwd"]}',
                                        f'cd {data["FOLDER_E"]}; ls -l | grep "^d"',
                                        folder))
            for item in value:
                res.append(ssh_checkout(f'{data["ip"]}',
                                        f'{data["user"]}',
                                        f'{data["passwd"]}',
                                        f'cd {data["FOLDER_E"]}; ls -l | grep "^-"',
                                        item))
        assert all(res), 'test2 FAIL'

    def test_step3(self, make_files):
        # test3
        res = [ssh_checkout(f'{data["ip"]}',
                            f'{data["user"]}',
                            f'{data["passwd"]}',
                            f'cd {data["OUT"]}; 7z x arx2.{data["type"]} -o{data["FOLDER_X"]} -y',
                            'Everything is Ok')]
        folder = ''
        for key, value in make_files.items():
            if key != data['TST']:
                *_, folder = key.split('/')
            for item in value:
                res.append(ssh_checkout(f'{data["ip"]}',
                                        f'{data["user"]}',
                                        f'{data["passwd"]}',
                                        f'cd {data["FOLDER_X"]}/{folder}; ls -l | grep "^-"',
                                        item))
        assert all(res), 'test3 FAIL'

    def test_step4(self):
        # test4
        assert ssh_checkout(f'{data["ip"]}',
                            f'{data["user"]}',
                            f'{data["passwd"]}',
                            f'cd {data["OUT"]}; 7z t arx2.{data["type"]}',
                            'Everything is Ok'), 'test4 FAIL'

    def test_step5(self, make_files):
        # test5
        res = []
        folder = ''
        for key, value in make_files.items():
            if key != data['TST']:
                *_, folder = str(key.split('/')) + '/'
            for item in value:
                res.append(ssh_checkout(f'{data["ip"]}',
                                        f'{data["user"]}',
                                        f'{data["passwd"]}',
                                        f'cd {data["OUT"]}; 7z l arx2.{data["type"]}',
                                        f'{folder}{item}'))
        res.append(ssh_checkout(f'{data["ip"]}',
                                f'{data["user"]}',
                                f'{data["passwd"]}',
                                f'cd {data["OUT"]}; 7z l arx2.{data["type"]}',
                                ' 5 files,'))
        res.append(ssh_checkout(f'{data["ip"]}',
                                f'{data["user"]}',
                                f'{data["passwd"]}',
                                f'cd {data["OUT"]}; 7z l arx2.{data["type"]}',
                                ' 1 folders'))
        assert all(res), 'test5 FAIL'

    def test_step6(self):
        result_out_7z = ssh_getout(f'{data["ip"]}',
                                   f'{data["user"]}',
                                   f'{data["passwd"]}',
                                   f'cd {data["OUT"]}; 7z h arx2.{data["type"]}')
        for elm in result_out_7z.split('\n'):
            if 'CRC32  for data:' in elm:
                *_, hash_7z = elm.split()
                break
        else:
            hash_7z = None
        hash_crc32 = ssh_getout(f'{data["ip"]}',
                                f'{data["user"]}',
                                f'{data["passwd"]}',
                                f'cd {data["OUT"]}; crc32 arx2.{data["type"]}')
        assert hash_7z.lower() == hash_crc32[:-1], 'test6 FAIL'

    def test_step7(self):
        # test7
        assert ssh_checkout(f'{data["ip"]}',
                            f'{data["user"]}',
                            f'{data["passwd"]}',
                            f'cd {data["TST"]}; 7z u {data["OUT"]}/arx2.{data["type"]}',
                            'Everything is Ok'), 'test7 FAIL'

    def test_step8(self):
        # test8
        assert ssh_checkout(f'{data["ip"]}',
                            f'{data["user"]}',
                            f'{data["passwd"]}',
                            f'cd {data["OUT"]}; 7z d arx2.{data["type"]}',
                            'Everything is Ok'), 'test8 FAIL'
