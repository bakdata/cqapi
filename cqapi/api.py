from aiohttp import ClientSession
from aiohttp import ClientConnectorError
from cqapi import util
import csv

class CqApiError(BaseException):
    pass


class ConqueryClientConnectionError(CqApiError):
    def __init__(self, msg):
        self.message = msg


async def get(session, url):
    async with session.get(url) as response:
        return await response.json()


async def get_text(session, url):
    async with session.get(url) as response:
        return await response.text()


async def post(session, url, data):
    async with session.post(url, json=data) as response:
        return await response.json()


class ConqueryConnection(object):
    async def __aenter__(self):
        self._session = ClientSession()
        # try to fail early if conquery is not available at self._url
        if self._check_connection:
            try:
                await self.get_datasets()
            except ClientConnectorError:
                error_msg = f"Could not connect to Conquery, are you sure {self._url} is the right address?"
                raise ConqueryClientConnectionError(error_msg)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    def __init__(self, url, requests_timout=5, check_connection = True):
        self._url = url.strip('/')
        self._check_connection = check_connection
        self._timeout = requests_timout

    async def get_datasets(self):
        response_list = await get(self._session, f"{self._url}/api/datasets")
        return [d['id'] for d in response_list]

    async def get_concepts(self, dataset):
        response = await get(self._session, f"{self._url}/api/datasets/{dataset}/concepts")
        return response['concepts']

    async def get_concept(self, dataset, concept_id):
        response_dict = await get(self._session, f"{self._url}/api/datasets/{dataset}/concepts/{concept_id}")
        response_list = [dict(attrs, **{"ids": [c_id]}) for c_id, attrs in response_dict.items()]
        return response_list

    async def get_stored_queries(self, dataset):
        response_list = await get(self._session, f"{self._url}/api/datasets/{dataset}/stored-queries")
        return response_list

    async def get_stored_query(self, dataset, query_id):
        result = await get(self._session, f"{self._url}/api/datasets/{dataset}/stored-queries/{query_id}")
        return result.get('query')

    async def get_query(self, dataset, query_id):
        result = await get(self._session, f"{self._url}/api/datasets/{dataset}/queries/{query_id}")
        return result

    async def execute_query(self, dataset, query):
        result = await post(self._session, f"{self._url}/api/datasets/{dataset}/queries", query)
        try:
            return result['id']
        except KeyError:
            raise ValueError("Error encountered when executing query", result.get('message'), result.get('details'))

    async def get_query_result(self, dataset, query_id):
        """ Returns results for given query.
        Blocks until the query is DONE.

        :param dataset:
        :param query_id:
        :return: str containing the returned csv's
        """
        response = await self.get_query(dataset, query_id)
        while not response['status'] == 'DONE':
            response = await self.get_query(dataset, query_id)

        result_string = await self._download_query_results(response["resultUrl"])
        return list(csv.reader(result_string.splitlines(), delimiter=';'))

    async def _download_query_results(self, url):
        return await get_text(self._session, url)

    async def create_concept_query_with_selects(self, dataset: str, concept_id: str, selects: list=None):
        concepts = await self.get_concepts(dataset)

        if selects is None:
            selects = util.selects_per_concept(concepts).get(concept_id)

        concept_query = util.concept_query_from_concept(concept_id, concepts.get(concept_id))
        return util.add_selects_to_concept_query(concept_query, concept_id, selects)

