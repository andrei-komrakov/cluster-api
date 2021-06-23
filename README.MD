#### Swisscom Assignment

### 1. Description
Project consists from 2 separate services.

Connector is the main API which would be exposed to the public.
It delegates the manipulations over the Group entity to the Node service.
Node service and its replicas function as a cluster with completely independent nodes.
Connector synchronizes the data between the nodes.

### 2. Installation and running
#### 2.1 Docker
Docker-compose file is configured to run the Connector APi Service and 3 Nodes.
`.env.docker.example` in `connector` folder contains ready to use env config and can be renamed to `.env.docker` which will be used by docker.

After `.env.docker` is configured or copied from `.env.docker.example` the project can be started
via Make

```shell
make run
```

or simply using `docker-compose.yml` file directly

```shell
docker-compose up
```

#### 2.2 Local environment
Project dependencies are managed by Pipenv. `cd` into the `connector` or `node` service and run

```shell
pipenv install
```

which will install the dependencies and creates a virtual env.

---

Alternatively

```shell
pip install -r requirements.txt
```

can be used to install the dependencies. In this case virtual environment should be configured manually.
This project targets Python 3.9+

#### 2.2+ Running in local environment
Connector configuration is managed by `.env.example` file.
To run, `cd` into the appropriate application and execute

```shell
uvicorn app.api:app --host 8000
```

Nodes should use a different port and all nodes' port should be specified in connector's `.env` file

### 3. API docs

Once API is running, docs can be accessed by `/v1/docs` and `/v1/redoc` url

### 4. Tests

#### 4.1 Docker environment

Test can be executed by Make

```shell
make test
```

or executed directly via docker container

```shell
docker-compose run api python -m pytest tests
docker-compose run node1 python -m pytest tests
```

#### 4.2 Local environment

Tests are managed by `pytest` and can be executed with

```shell
python -m pytest tests
```

command in the appropriate service folder

### 5. Generator command
#### 5.1 Docker environment
To run a script which generates a number of group, simple execute

```shell
make generate
```

#### 5.2 Local environment
Make sure connector and nodes are configured. After that run

```shell
python3 -m app.cli
```

command supports an optional number which indicates the number of group which will be created

```shell
python3 -m app.cli --amount 3000
```

### 6. Concerns
- no authentication in main api and internal api
- internal api can be rewritten to grpc os similar protocol to enhance security and optimization
- internal api relies on HTTP status which is not accurate
- self-written store can be replaced with a 3rd party solution. For example postgres with synchronous_commit=remote_apply, several replica nodes and waiting for all of them to acknowledge the write
- the queue of intentions in node server is not being clean right now. In-memory worker or using 3rd party storage with TTL or Leases can solve this issue
