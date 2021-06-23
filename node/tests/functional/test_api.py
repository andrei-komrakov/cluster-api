from uuid import uuid4

from fastapi.testclient import TestClient

import app.store as store
from app.api import app
from tests.helper import freeze_store


class TestGet:
    @freeze_store
    def test_happy_path(self):
        group_id = 'test_group'
        store.store = {group_id: group_id}

        client = TestClient(app)
        response = client.get(f'/v1/group/{group_id}')

        assert 200 == response.status_code
        assert {'groupId': group_id} == response.json()

    @freeze_store
    def test_not_found(self):
        group_id = 'test_group'

        client = TestClient(app)
        response = client.get(f'/v1/group/{group_id}')

        assert 404 == response.status_code


class TestPost:
    @freeze_store
    def test_happy_path(self):
        group_id = 'test_group'
        session_id = str(uuid4())

        assert group_id not in store.store, 'initial check'

        client = TestClient(app)
        response = client.post('/v1/group', json={'groupId': group_id, 'sessionId': session_id})

        assert 200 == response.status_code
        assert group_id not in store.store, 'first call to add a group should only record the intention'
        assert group_id in store.diff, 'first call to add a group should record the intention'

        response = client.post('/v1/group', json={'groupId': group_id, 'sessionId': session_id})

        assert 200 == response.status_code
        assert group_id in store.store, 'second call to add a new group with the same sessionId should be successful'
        assert group_id not in store.diff, 'second call to add a group should erase group_id from intention list'

    @freeze_store
    def test_existing_group(self):
        group_id = 'test_group'
        session_id = str(uuid4())

        store.store = {group_id: group_id}

        client = TestClient(app)
        response = client.post('/v1/group', json={'groupId': group_id, 'sessionId': session_id})

        assert 409 == response.status_code


class TestDelete:
    @freeze_store
    def test_happy_path(self):
        group_id = 'test_group'
        session_id = str(uuid4())

        store.store = {group_id: group_id}

        client = TestClient(app)
        response = client.delete(f'/v1/group/{group_id}', json={'sessionId': session_id})

        assert 200 == response.status_code
        assert group_id in store.store, 'first call to remove should only store an intention to remove a group id'
        assert group_id in store.diff, 'first call to remove should record an intention to remove a group id'

        response = client.delete(f'/v1/group/{group_id}', json={'sessionId': session_id})

        assert 200 == response.status_code
        assert group_id not in store.store, 'second call to remove should remove a group id'
        assert group_id not in store.diff, 'second call to remove should remove group id from the intention list'

    @freeze_store
    def test_handles_missing_group_id(self):
        group_id = 'test_group'
        session_id = str(uuid4())

        assert group_id not in store.store, 'initial check'

        client = TestClient(app)
        response = client.delete(f'/v1/group/{group_id}', json={'sessionId': session_id})

        assert 404 == response.status_code
