from cqapi import ConqueryConnection
from cqapi import ConqueryClientConnectionError
import pytest
import json
import os


tests_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(tests_dir, 'resources', 'tests.json')

with open(file_path) as fp:
    tests_json = json.load(fp)

base_url = "http://localhost:9085"


# Helpers


def build_test_parametrization(tests_json):
    test_params = []
    for api_method in tests_json.keys():
        print(api_method)
        for test_def in tests_json.get(api_method):
            assert(dict == type(test_def))
            print(test_def)
            test_params.append((
                api_method,
                test_def.get("method_params"),
                test_def.get("mocked_backend"),
                test_def.get("expected_result")
            ))
    print(test_params)
    return test_params


def create_get_mock(mocked_backend):
    results_by_endpoint = {d.get("endpoint"): d.get("result") for d in mocked_backend}

    async def mocked_get(__, url):
        if url[len(base_url):] in results_by_endpoint.keys():
            return results_by_endpoint.get(url[len(base_url):])
        else:
            raise Exception(f"Badly configured test queried url {url}, but endpoints {[base_url + endpoint for endpoint in results_by_endpoint.keys()]} was configured.")

    return mocked_get


def create_post_mock(mocked_backend):
    results_by_endpoint = {d.get("endpoint"): d.get("result") for d in mocked_backend}

    async def mocked_post(__, url, ___):
        if url[len(base_url):] in results_by_endpoint.keys():
            return results_by_endpoint.get(url[len(base_url):])
        else:
            raise Exception(f"Badly configured test queried url {url}, but endpoints {[base_url + endpoint for endpoint in results_by_endpoint.keys()]} was configured.")

    return mocked_post


def create_get_text_mock(mocked_backend):
    results_by_endpoint = {d.get("endpoint"): d.get("result") for d in mocked_backend if d.get("type") == "csv"}

    async def mocked_get_text(__, url):
        if url[len(base_url):] in results_by_endpoint.keys():
            return results_by_endpoint.get(url[len(base_url):])
        else:
            raise Exception(f"Badly configured test queried url {url}, but endpoints {[base_url + endpoint for endpoint in results_by_endpoint.keys()]} was configured.")

    return mocked_get_text


# ConqueryConnection init test

@pytest.mark.asyncio
async def test_cq_conn_init():
    with pytest.raises(ConqueryClientConnectionError):
        async with ConqueryConnection(base_url) as cq:
            pass


# Backend mock fixture


@pytest.fixture(name='mock_backend')
def mock_backend(mocker, api_method, method_params, mocked_backend, expected_result):
    mocker.patch('cqapi.api.get', side_effect=create_get_mock(mocked_backend))
    mocker.patch('cqapi.api.post', side_effect=create_post_mock(mocked_backend))
    mocker.patch('cqapi.api.get_text', side_effect=create_get_text_mock(mocked_backend))

# Tests


tests = build_test_parametrization(tests_json)


@pytest.mark.usefixtures('mock_backend')
@pytest.mark.asyncio
@pytest.mark.parametrize("api_method, method_params, mocked_backend, expected_result", tests)
async def test_api_methods(api_method, method_params, expected_result):
    async with ConqueryConnection(base_url, check_connection=False) as cq:
        method_under_test = getattr(cq, api_method)
        result = await method_under_test(*method_params)
        assert expected_result == result

