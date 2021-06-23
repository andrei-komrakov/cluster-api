from uuid import uuid4

import pytest

import app.store as store
from app.exceptions import DuplicatingGroupError, GroupInUpdateError, NotFoundError
from tests.helper import freeze_store_async


class TestAdd:
    @pytest.mark.asyncio
    @freeze_store_async
    async def test_happy_path(self):
        group_id = "test_group_id"
        session_id = str(uuid4())

        assert group_id not in store.store, 'initial check'

        await store.add(group_id, session_id)
        assert group_id not in store.store, 'first call to add should only store an intention to add a group id'
        assert group_id in store.diff, 'first call to add should record an intention to add a group id'

        await store.add(group_id, session_id)
        assert group_id in store.store, 'second call to add should record a group id'
        assert group_id not in store.diff, 'second call to add should remove group id from the intention list'

    @pytest.mark.asyncio
    @freeze_store_async
    async def test_fails_to_simultaneously_add_a_group(self):
        group_id = "test_group_id"
        session_id = str(uuid4())

        assert group_id not in store.store, 'initial check'

        await store.add(group_id, session_id)
        assert group_id not in store.store, 'first call to add should only store an intention to add a group id'
        assert group_id in store.diff, 'first call to add should record an intention to add a group id'

        competing_session_id = str(uuid4())
        with pytest.raises(GroupInUpdateError):
            await store.add(group_id, competing_session_id)

    @pytest.mark.asyncio
    @freeze_store_async
    async def test_handles_existing_group(self):
        group_id = "test_group_id"
        session_id = str(uuid4())

        assert group_id not in store.store, 'initial check'

        await store.add(group_id, session_id)
        assert group_id not in store.store, 'first call to add should only store an intention to add a group id'
        assert group_id in store.diff, 'first call to add should record an intention to add a group id'

        await store.add(group_id, session_id)
        assert group_id in store.store, 'second call to add should record a group id'
        assert group_id not in store.diff, 'second call to add should remove group id from the intention list'

        with pytest.raises(DuplicatingGroupError):
            await store.add(group_id, session_id)


class TestGet:
    @pytest.mark.asyncio
    @freeze_store_async
    async def test_happy_path(self):
        group_id = 'test_group_id'
        store.store = {group_id: group_id}

        assert group_id in store.store, 'initial check'

        result = await store.get(group_id)

        assert group_id == result, f'expected {group_id} got {result}'

    @pytest.mark.asyncio
    @freeze_store_async
    async def test_handles_missing_group_id(self):
        group_id = 'test_group_id'

        assert group_id not in store.store, 'initial check'

        with pytest.raises(NotFoundError):
            await store.get(group_id)


class TestDelete:
    @pytest.mark.asyncio
    @freeze_store_async
    async def test_happy_path(self):
        group_id = "test_group_id"
        session_id = str(uuid4())

        store.store = {group_id: group_id}

        assert group_id in store.store, 'initial check'

        await store.remove(group_id, session_id)
        assert group_id in store.store, 'first call to remove should only store an intention to remove a group id'
        assert group_id in store.diff, 'first call to remove should record an intention to remove a group id'

        await store.remove(group_id, session_id)
        assert group_id not in store.store, 'second call to remove should remove a group id'
        assert group_id not in store.diff, 'second call to remove should remove group id from the intention list'

    @pytest.mark.asyncio
    @freeze_store_async
    async def test_fails_to_simultaneously_delete_a_group(self):
        group_id = "test_group_id"
        session_id = str(uuid4())

        store.store = {group_id: group_id}

        assert group_id in store.store, 'initial check'

        await store.remove(group_id, session_id)
        assert group_id in store.store, 'first call to remove should only store an intention to remove a group id'
        assert group_id in store.diff, 'first call to remove should record an intention to remove a group id'

        competing_session_id = str(uuid4())
        with pytest.raises(GroupInUpdateError):
            await store.remove(group_id, competing_session_id)

    @pytest.mark.asyncio
    @freeze_store_async
    async def test_handles_missing_group_id(self):
        group_id = "test_group_id"
        session_id = str(uuid4())

        assert group_id not in store.store, 'initial check'

        with pytest.raises(NotFoundError):
            await store.remove(group_id, session_id)
