import pytest

from main import YaDiskApi, load_token


class TestYaDiskApi:
    dirs = ['dir1', 'dir2', 'dir3']
    
    # получить токен
    @pytest.fixture(autouse=True)
    def get_token(self):
        self.token = load_token()
        self.ya_disk_api = YaDiskApi(self.token)
        
    # проверить, что при создании папки код ответа соответствует 200
    @pytest.mark.parametrize(
        'dir,expected', [(dir, 201) for dir in dirs]
    )
    def test_status_code_ok(self, dir, expected):
        res = self.ya_disk_api.create_dir(dir)
        assert res == expected
    
    # проверить, что результат создания папки - папка появилась в списке файлов.
    @pytest.mark.parametrize(
        'dir,expected', [(dir, {'name': dir}) for dir in dirs]
    )
    def test_dir_on_disk(self, dir, expected):
        self.ya_disk_api.create_dir(dir)
        res = self.ya_disk_api.get_dir(dir)
        assert res == expected
    
    # проверка, что при создании двух папок с одним именем вернется код ответа 409
    @pytest.mark.parametrize(
        'dir,expected', [(dir, 409) for dir in dirs]
    )
    def test_dir_already_exists(self, dir, expected):
        res1 = self.ya_disk_api.create_dir(dir)
        res2 = self.ya_disk_api.create_dir(dir)
        assert res2 == expected