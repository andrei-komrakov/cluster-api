# this is needed to suppress grequests MonkeyPatchWarning warning
from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)

from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from app.api import app
from app.exceptions import GroupNotFoundError, NodeConnectionError


class TestGet:
    @patch('app.connector.grequests')
    def test_happy_path(self, mock_grequests: Mock):
        mock_grequests.imap = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock()

        mock_response.json.return_value = {'groupId': 'test'}
        mock_grequests.imap.return_value = [mock_response]

        client = TestClient(app)
        response = client.get('/v1/group/test')
        assert 200 == response.status_code
        assert {'groupId': 'test'} == response.json()

    @patch('app.api.Connector')
    def test_handles_node_connection_error(self, mock_connector: Mock):
        mock_connector_instance = Mock()
        mock_connector.return_value = mock_connector_instance
        mock_connector_instance.get = Mock()
        mock_connector_instance.get.side_effect = NodeConnectionError()

        client = TestClient(app)
        response = client.get('/v1/group/test')
        assert 503 == response.status_code

    @patch('app.api.Connector')
    def test_handles_missing_group_id(self, mock_connector: Mock):
        mock_connector_instance = Mock()
        mock_connector.return_value = mock_connector_instance
        mock_connector_instance.get = Mock()
        mock_connector_instance.get.side_effect = GroupNotFoundError()

        client = TestClient(app)
        response = client.get('/v1/group/test')
        assert 404 == response.status_code


class TestPost:
    @patch('app.connector.grequests')
    def test_post_happy_path(self, mock_grequests: Mock):
        mock_grequests.map = Mock()
        mock_grequests.imap = Mock()
        mock_response = Mock()
        mock_response.status_code = 200

        mock_grequests.map.return_value = [mock_response]
        mock_grequests.imap.return_value = [mock_response]

        client = TestClient(app)
        response = client.post('/v1/group', json={'groupId': 'test'})
        assert 201 == response.status_code

    @patch('app.api.Connector')
    def test_handles_node_connection_error(self, mock_connector: Mock):
        mock_connector_instance = Mock()
        mock_connector.return_value = mock_connector_instance
        mock_connector_instance.create = Mock()
        mock_connector_instance.create.side_effect = NodeConnectionError()

        client = TestClient(app)
        response = client.post('/v1/group', json={'groupId': 'test'})
        assert 503 == response.status_code


class TestDelete:
    @patch('app.connector.grequests')
    def test_delete_happy_path(self, mock_grequests: Mock):
        mock_grequests.map = Mock()
        mock_grequests.imap = Mock()
        mock_response = Mock()
        mock_response.status_code = 200

        mock_grequests.map.return_value = [mock_response]
        mock_grequests.imap.return_value = [mock_response]

        client = TestClient(app)
        response = client.delete('/v1/group/test', json={'groupId': 'test'})
        assert 200 == response.status_code

    @patch('app.api.Connector')
    def test_handles_node_connection_error(self, mock_connector: Mock):
        mock_connector_instance = Mock()
        mock_connector.return_value = mock_connector_instance
        mock_connector_instance.delete = Mock()
        mock_connector_instance.delete.side_effect = NodeConnectionError()

        client = TestClient(app)
        response = client.delete('/v1/group/test')
        assert 503 == response.status_code

    @patch('app.api.Connector')
    def test_handles_missing_group_id(self, mock_connector: Mock):
        mock_connector_instance = Mock()
        mock_connector.return_value = mock_connector_instance
        mock_connector_instance.delete = Mock()
        mock_connector_instance.delete.side_effect = GroupNotFoundError()

        client = TestClient(app)
        response = client.delete('/v1/group/test')
        assert 404 == response.status_code
