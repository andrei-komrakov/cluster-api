from http import HTTPStatus

from fastapi import Body, FastAPI, Response
from fastapi_versioning import VersionedFastAPI, version

from .connector import Connector

app = FastAPI(title='Swisscom assignment')


@app.get(
    '/group/{group_id}',
    summary='Retrieve a group',
    tags=['Group'],
    responses={
        200: {
            'description': 'Group details.',
            'content': {
                'application/json': {
                    'example': {'groupId': 'example-group-id'}
                }
            },
        },
        404: {
            'description': 'Group id not found.',
        },
        503: {
            'description': 'Service is unavailable.'
        },
    }
)
@version(1)
async def get(group_id: str):
    connector = Connector()

    result = await connector.get(group_id)
    return {"groupId": result}


@app.post(
    '/group',
    summary='Create new group',
    tags=['Group'],
    responses={
        201: {
            'description': 'Group successfully created.'
        },
        409: {
            'description': 'Group with specified id already exists or being created by someone else.'
        },
        503: {
            'description': 'Service unavailable.'
        }
    }
)
@version(1)
async def post(group_id: str = Body(..., alias='groupId', embed=True)):
    connector = Connector()
    await connector.create(group_id)

    return Response(status_code=HTTPStatus.CREATED)


@app.delete(
    '/group/{group_id}',
    summary='Delete a group',
    tags=['Group'],
    responses={
        200: {
            'description': 'Group was successfully deleted.'
        },
        404: {
            'description': 'Group id not found.',
        },
        409: {
            'description': 'Group with this id is being deleted by someone else.'
        },
        503: {
            'description': 'Service is unavailable.'
        },
    }
)
@version(1)
async def delete(group_id: str):
    connector = Connector()
    await connector.delete(group_id)


app = VersionedFastAPI(
    app,
    version_format='{major}',
    prefix_format='/v{major}')
