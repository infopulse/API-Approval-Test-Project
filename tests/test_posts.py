from pytest import mark


# simple test
def test_get_posts(session, verify):
    response = session.get('/posts')
    verify(response.json())


def test_get_post_by_id_1(session, verify):
    response = session.get('/posts/1')
    verify(response.json())


def test_get_post_by_id_2(session, verify):
    response = session.get('/posts/2')
    verify(response.json())


# parametrized test
@mark.parametrize('post_id', [3, 4, 5])
def test_get_post_by_id(session, verify, post_id):
    response = session.get(f'/posts/{post_id}')
    verify(response.json())


# test with multiple, non json assertions
def test_check_post_details(session, verify):
    response = session.get('/posts/6')
    title = response.json()['title']
    body = response.json()['body']
    verify(title)
    verify(body)


# test status codes
def test_get_posts_status_code(session, verify):
    response = session.get('/posts/222')
    verify(response.status_code)
