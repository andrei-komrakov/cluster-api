from asyncio import Lock

from app.exceptions import DuplicatingGroupError, GroupInUpdateError, NotFoundError

store = dict()
diff = dict()
lock = Lock()


async def add(group_id: str, session_id: str):
    async with lock:
        if group_id in store:
            raise DuplicatingGroupError

        if group_id in diff:
            if diff[group_id][0] != session_id:
                raise GroupInUpdateError
            store[group_id] = group_id
            diff.pop(group_id)
        else:
            diff[group_id] = [session_id, group_id]


async def remove(group_id: str, session_id: str):
    async with lock:
        if group_id not in store:
            raise NotFoundError

        if group_id in diff:
            if diff[group_id][0] != session_id:
                raise GroupInUpdateError
            store.pop(group_id)
            diff.pop(group_id)
        else:
            diff[group_id] = [session_id, group_id]


async def get(group_id: str) -> str:
    if group_id not in store:
        raise NotFoundError

    return store[group_id]
