from http import HTTPStatus
from uuid import uuid4

import grequests

from .config import HOSTS, TIMEOUT
from .exceptions import GroupNotFoundError, NodeConnectionError


class Connector:
    async def create(self, group_id: str):
        session_id = uuid4()
        requests = [grequests.post(
            self._format_post(host),
            timeout=TIMEOUT,
            json={'groupId': group_id, 'sessionId': str(session_id)})
            for host in HOSTS]

        # wait for all requests to complete since we need a confirmation
        for response in grequests.map(requests):
            # non OK response actually treated as `response == False` hence the explicit check for None
            if response == None:
                raise NodeConnectionError

            if response.status_code != HTTPStatus.OK:
                raise NodeConnectionError

        # use a generator to traverse through the responses as soon as it is received
        for response in grequests.imap(requests):
            if not response or response.status_code != HTTPStatus.OK:
                raise NodeConnectionError

    async def delete(self, group_id: str):
        session_id = uuid4()
        requests = [grequests.delete(
            self._format_get(host, group_id),
            timeout=TIMEOUT,
            json={'sessionId': str(session_id)})
            for host in HOSTS]

        # wait for all requests to complete since we need a confirmation
        for response in grequests.map(requests):
            if response == None:
                raise NodeConnectionError

            if response.status_code == HTTPStatus.NOT_FOUND:
                raise GroupNotFoundError

            if response.status_code != HTTPStatus.OK:
                raise NodeConnectionError

        # use a generator to traverse through the responses as soon as it is received
        for response in grequests.imap(requests):
            if not response or response.status_code != HTTPStatus.OK:
                raise NodeConnectionError

    async def get(self, group_id: str) -> str:
        requests = [grequests.get(self._format_get(host, group_id), timeout=TIMEOUT) for host in HOSTS]
        for response in grequests.imap(requests):
            if response == None:
                continue

            if response.status_code == HTTPStatus.NOT_FOUND:
                raise GroupNotFoundError()

            if response.status_code == HTTPStatus.OK:
                json = response.json()
                return json['groupId']

        raise NodeConnectionError

    @classmethod
    def _format_get(cls, host: str, group_id: str) -> str:
        return '{host}/v1/group/{group_id}'.format(host=host, group_id=group_id)

    @classmethod
    def _format_post(cls, host: str) -> str:
        return '{host}/v1/group'.format(host=host)
