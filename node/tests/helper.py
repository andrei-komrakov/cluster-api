import functools

import app.store as store


def freeze_store(func):
    def wrapper(*args, **kwargs):
        initial_store = dict(store.store)
        initial_diff = dict(store.diff)

        result = func(*args, **kwargs)

        store.store = initial_store
        store.diff = initial_diff

        return result
    return wrapper


def freeze_store_async(func):
    async def wrapper(*args, **kwargs):
        initial_store = dict(store.store)
        initial_diff = dict(store.diff)

        result = await func(*args, **kwargs)

        store.store = initial_store
        store.diff = initial_diff

        return result
    return wrapper
