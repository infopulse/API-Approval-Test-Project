# regular tests
def test_get_comments(session):
    response = session.get('/posts/1/comments')
    assert response.status_code == 200
    assert len(response.json()) == 5

# approval tests
def test_get_comments(session, verify):
    response = session.get('/posts/1/comments')
    verify(response.json())


def test_get_comment_by_post_id(session, verify):
    response = session.get('/comments?postId=1')
    verify(response.json())
