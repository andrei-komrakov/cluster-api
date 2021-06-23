import argparse
import asyncio
from uuid import uuid4

from .connector import Connector


async def generate(group_id: str) -> bool:
    connector = Connector()

    try:
        await connector.create(group_id)
        return True
    except:
        return False


async def verify(group_id: str) -> bool:
    connector = Connector()

    try:
        await connector.get(group_id)
        return True
    except:
        return False


async def process(number_of_groups: int):
    successful = 0
    failed = 0
    verified = 0
    group_ids = []

    print(f'producing {number_of_groups} groups')
    for i in range(number_of_groups):
        if i % 100 == 0:
            print(f'{i} out of {number_of_groups}')

        group_id = str(uuid4())
        result = await generate(group_id)

        if result:
            successful += 1
            group_ids.append(group_id)
        else:
            failed += 1

    print(f'Successful queries: {successful}')
    print(f'Failed queries: {failed}')

    print(f'Starting verification')
    for i, group_id in enumerate(group_ids):
        if i % 100 == 0:
            print(f'{i} out of {len(group_ids)}')
        result = await verify(group_id)

        if result:
            verified += 1

    print(f'{verified} out of {len(group_ids)} are successfully verified')


parser = argparse.ArgumentParser()
parser.add_argument(
    '-a', '--amount',
    dest='amount', type=int, nargs='?',
    help='query string', default='1000')

args = parser.parse_args()
amount = int(args.amount)

loop = asyncio.get_event_loop()
loop.run_until_complete(process(amount))
loop.close()
