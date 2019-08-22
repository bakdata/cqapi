from cqapi import ConqueryConnection
from cqapi.util import dict_to_object
import pytest
import json
import os


tests_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(tests_dir, 'resources', 'endpoints.json')

with open(file_path) as fp:
    endpoint_config = json.load(fp, object_hook=dict_to_object)

base_url = endpoint_config['base_url']

# Helpers

def get_expected(url):
    return endpoint_config["get_endpoints"][url]["expected"]


async def mocked_get(__, url):
    offset = len(base_url)
    return endpoint_config['get_endpoints'][url[offset:]]["cq_result"]


@pytest.fixture(name="mock_backend")
def mocked_backend(mocker):
    mocker.patch('cqapi.api.get', side_effect=mocked_get)
    mocker.patch('cqapi.api.post', side_effect=mocked_get)

# Tests

@pytest.mark.asyncio
async def test_cq_connection_init(mock_backend):
    """
    Tests the initialization of a ConqueryConnection.
    Expects CQ backend to be running on localhost:8080.
    """
    async with ConqueryConnection(base_url) as cq:
        assert(isinstance(cq, ConqueryConnection))


# todo add these endpoint tests to endpoints.json
"""
@pytest.mark.asyncio
async def test_get_running_query(mock_backend):
    async with ConqueryConnection(base_url) as cq:
        running_query = await cq.get_query("demo", "demo.running_query")
        assert get_expected("/api/datasets/demo/queries/demo.running_query") == running_query

@pytest.mark.asyncio
async def test_get_finished_query(mock_backend):
    async with ConqueryConnection(base_url) as cq:
        finished_query = await cq.get_query("demo", "demo.finished_query")
        assert get_expected("/api/datasets/demo/queries/demo.finished_query") == finished_query
        
@pytest.mark.asyncio
async def test_get_query_result(mock_backend):
    async with ConqueryConnection(base_url) as cq:
        finished_query = await cq.get_query_result("demo", "demo.finished_query")
        assert get_expected("/api/datasets/demo/queries/demo.finished_query") == finished_query
"""

get_endpoint_tests = [(value["api_method_name"],
                       value["api_method_params"],
                       value["expected"])
                       for key, value in endpoint_config['get_endpoints'].items()]


@pytest.mark.asyncio
@pytest.mark.parametrize("cq_method, cq_method_params, expected", get_endpoint_tests)
async def test_get_endpoint_wrappers(mock_backend, cq_method, cq_method_params, expected):
    async with ConqueryConnection(base_url) as cq:
        method_under_test = getattr(cq, cq_method)
        result = await method_under_test(*cq_method_params)
        assert expected == result

