from http import HTTPStatus

from fastapi import Body, FastAPI, HTTPException, Path
from fastapi_versioning import VersionedFastAPI, version

import app.store as store
from app.exceptions import DuplicatingGroupError, GroupInUpdateError, NotFoundError

app = FastAPI()


@app.get('/group/{group_id}')
@version(1)
async def get(group_id: str):
    try:
        result = await store.get(group_id)
        return {'groupId': result}
    except NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail={'error': 'Group id does not exist'})
    except:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail={'error': 'Something went wrong'})


@app.delete('/group/{group_id}')
@version(1)
async def delete(
        group_id: str = Path(...),
        session_id: str = Body(..., embed=True, alias='sessionId')):
    try:
        await store.remove(group_id, session_id)
    except NotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail={'error': f'Group "{group_id}" does not exist'})
    except GroupInUpdateError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail={'error': f'Group "{group_id}" is being updated'})
    except:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.post('/group')
@version(1)
async def post(
        group_id: str = Body(..., embed=True, alias='groupId'),
        session_id: str = Body(..., embed=True, alias='sessionId')):
    try:
        await store.add(group_id, session_id)
    except DuplicatingGroupError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail={'error': f'Group "{group_id}" already exists'})
    except GroupInUpdateError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail={'error': f'Group "{group_id}" is being updated'})
    except:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


app = VersionedFastAPI(
    app,
    version_format='{major}',
    prefix_format='/v{major}')
