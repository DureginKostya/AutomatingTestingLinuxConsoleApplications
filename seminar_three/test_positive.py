import yaml
from checkers import checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_step1(self):
        # test1
        result1 = checkout(f'cd {data["TST"]}; '
                           f'7z a {data["OUT"]}/arx2 -t{data["type"]}',
                           'Everything is Ok')
        result2 = checkout(f'cd {data["OUT"]}; ls', f'arx2.{data["type"]}')
        assert result1 and result2, 'test1 FAIL'

    def test_step2(self, make_files):
        # test2
        result = [checkout(f'cd {data["OUT"]}; '
                           f'7z e arx2.{data["type"]} -o{data["FOLDER_E"]} -y',
                           'Everything is Ok')]
        for item in make_files:
            result.append(checkout(f'cd {data["FOLDER_E"]}; ls', item))
        assert all(result), 'test2 FAIL'

    def test_step4(self):
        # test4
        assert checkout(f'cd {data["OUT"]}; 7z t arx2.{data["type"]}', 'Everything is Ok'), 'test4 FAIL'

    def test_step7(self):
        # test7
        assert checkout(f'cd {data["TST"]}; 7z u {data["OUT"]}/arx2.{data["type"]}', 'Everything is Ok'), 'test7 FAIL'

    def test_step8(self):
        # test8
        assert checkout(f'cd {data["OUT"]}; 7z d arx2.{data["type"]}', 'Everything is Ok'), 'test8 FAIL'
