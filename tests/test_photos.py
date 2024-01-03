from pytest import mark


@mark.parametrize('photo_id', [3, 4, 5, 6, 7, 8, 9, 10])
def test_get_photo_by_id(session, verify, photo_id):
    response = session.get(f'/photos/{photo_id}')
    verify(response.json())
