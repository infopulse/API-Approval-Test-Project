import os
import pytest
from dotenv import load_dotenv
from pytest import fixture
from pytest import Parser, FixtureRequest
from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
from base_session import BaseSession as Session


@fixture(scope='session', autouse=True)
def setup_env_variables():
    load_dotenv()


def pytest_addoption(parser: Parser):
    parser.addoption('--base-url', action='store', help='Specify web app URL to test')
    parser.addoption('--db', action='store', default='expected_results.json',
                     help='Specify path to database with expected results')


@fixture(scope='session')
def precondition(request: FixtureRequest):
    db_name = request.config.getoption('--db')
    dp_path = os.path.join(request.session.fspath.strpath, db_name)
    nosqldb = TinyDB(dp_path, storage=CachingMiddleware(JSONStorage))
    with nosqldb as db:
        yield db
    nosqldb.close()


@fixture(scope='function')
def verify(request: FixtureRequest, precondition):
    test = Query()
    identity = {'name': request.node.name, 'path': request.node.fspath.strpath, 'counter': 0}

    def inner(actual_result, ignored_keys: list[str] = None):
        ignored_keys = ignored_keys or []
        identity['counter'] += 1
        result = precondition.search(
            (test.name == identity['name']) & (test.path == identity['path']) & (test.counter == identity['counter']))
        if len(result) == 0:
            identity['result'] = clear_redundant_json(actual_result, ignored_keys)
            precondition.insert(identity)
        else:
            assert result[0]['result'] == clear_redundant_json(actual_result, ignored_keys)

    yield inner


@fixture(scope='session')
def session(request: FixtureRequest):
    token = os.getenv('SECRET_TOKEN')
    base_url = request.config.getoption('--base-url')
    if token is None:
        pytest.exit('SECRET_TOKEN is not set in the environment variable')
    if base_url is None:
        pytest.exit('BASE_URL is not set in CLI arguments')
    session = Session(base_url=base_url)
    session.base_url = os.getenv('BASE_URL', 'https://jsonplaceholder.typicode.com')
    session.headers.update({'Authorization': token,
                            'User-Agent': 'requests session'})
    yield session
    session.close()


# HELPERS
def clear_redundant_json(data, redundant: list[str]):
    new = type(data)()
    if isinstance(data, dict):
        for key, value in data.items():
            if key not in redundant:
                if isinstance(value, dict) or isinstance(value, list):
                    new[key] = clear_redundant_json(value, redundant)
                else:
                    new[key] = value
    elif isinstance(data, list):
        for i in data:
            if not isinstance(i, dict) and not isinstance(i, list):
                new.append(i)
            else:
                new.append(clear_redundant_json(i, redundant))
    else:
        return data
    return new
