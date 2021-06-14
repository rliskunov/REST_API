from videoblog import client
from videoblog.models import Video


def test_get():
    res = client.get('/tutorials')

    assert res.status_code == 200

    assert len(res.get_json()) == len(Video.query.all())
    assert res.get_json()[0]['id'] == 1


def test_post():
    data: dict[str, str] = {
        'name': 'Unit Tests POST',
        'description': 'Pytest tutorial'
    }

    res = client.post('/tutorials', json=data)

    assert res.status_code == 200


def test_put():
    data: dict[str, str] = {
        'name': 'Unit Tests PUT',
        'description': 'Pytest tutorial'
    }
    res = client.put('/tutorials/1', json=data)

    assert res.status_code == 200
    assert Video.query.get(1).name == 'Unit Tests PUT'


def test_delete():
    res = client.delete('/tutorials/1')

    assert res.status_code == 204
    assert Video.query.get(1) is None
