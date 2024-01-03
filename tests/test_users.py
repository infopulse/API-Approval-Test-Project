def test_user_by_id(session, verify):
    response = session.get('/users/1')
    verify(response.json(), ['email', 'city', 'geo'])
