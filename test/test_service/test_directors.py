from unittest.mock import MagicMock

import pytest

from dao.model.director import Director
from dao.director import DirectorDAO
from service.director import DirectorService


@pytest.fixture()  # "псевдо" "мокированное" DAO
def director_dao():
    director_dao = DirectorDAO(None)

    director1 = Director(
        id=1,
        name="Квентин Тарантино"
    )

    director2 = Director(
        id=2,
        name="Сергей Бодров"
    )

    director3 = Director(
        id=3,
        name="Никита Михалков"
    )

    director_dao.get_one = MagicMock(return_value=director1)
    director_dao.get_all = MagicMock(return_value=[director1, director2, director3])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert len(directors) > 0
        assert isinstance(directors, list)

    def test_create(self):
        new_director = {
            "id": 4,
            "name": "Джеки Чан"
        }
        director = self.director_service.create(new_director)
        assert director.id is not None

    def test_update(self):
        director_update = {
            "id": 1,
            "name": "Дарья Гладких"
        }
        self.director_service.update(director_update)

    def test_delete(self):
        self.director_service.delete(3)
