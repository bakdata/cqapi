from cqapi import ConqueryConnection
from cqapi.util import dict_to_object
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
                test_def.get("mocked_endpoint"),
                test_def.get("mocked_result"),
                test_def.get("expected_result")
            ))
    return test_params


def create_get_mock(endpoint, result):
    async def mocked_get(__, url):
        if url == base_url + endpoint:
            return result
        else:
            raise Exception(f"Badly configured test queried url {url}, but {base_url + endpoint} was configured.")
    return mocked_get


# Backend mock fixture


@pytest.fixture(autouse=True)
def mocked_backend(mocker, mocked_endpoint, mocked_result):
    mocker.patch('cqapi.api.get', side_effect=create_get_mock(mocked_endpoint, mocked_result))

# Tests

tests = build_test_parametrization(tests_json)


@pytest.mark.asyncio
@pytest.mark.parametrize("api_method, method_params, mocked_endpoint, mocked_result, expected_result", tests)
async def test_get_endpoint_wrappers(api_method, method_params, mocked_endpoint, mocked_result, expected_result):
    async with ConqueryConnection(base_url) as cq:
        method_under_test = getattr(cq, api_method)
        result = await method_under_test(*method_params)
        assert expected_result == result

