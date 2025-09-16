# Deals Finder

Simple deals finder with authentication.
Data are retrieved from Cheap Shark API.

## Requirements

To run this project you need:

`Poetry`:

    https://python-poetry.org/docs/#installation

And `pyenv`:

    https://github.com/pyenv/pyenv?tab=readme-ov-file#installation

And `node` and `pnpm` for FE :

    Node can be installed by your Package manager (apt, pacmac, dnf) or using NVM(Node versione manager) 
    
    https://github.com/nvm-sh/nvm?tab=readme-ov-file#install--update-script

And `docker` for DB:
    
    https://docs.docker.com/get-started/
    
    https://docs.docker.com/engine/install/

## Postgres container and .env.docker

After installing Docker and Docker Compose, it possible to run  postgres DB container navigate to the root directory and run the command:

    docker compose docker-compose.yml -d

That run a container with postgres server and detach the terminal from this.

You can setup postgres server by editing the parameter in the file

    .env.docker

## Development

Installing python envirorment using pyenv

    pyenv install $python-version

Setup pyenv local envirorment running this comand in backend folder

    pyenv local $python-version

To setup the environment for development, set the env with poetry:

    $ poetry env use $(pyenv which python)

Now it's possible to install the dependencies:

    $ poetry install

Then start the db:

    $ docker compose docker-compose.yml -d

Initialize the database schema with:

    $ poetry run python manage.py migrate

Initialize the data importing data from api:

    $ poetry run python manage.py fetch_deals 

Run the local web server:

    $ poetry run python manage.py runserver

The frontend is served at: [http://localhost:5173](http://localhost:5173) (see Frontend development and build)

## Running the tests

From backend folder run the tests:

    $ poetry run pytest


## Frontend development and build

The frontend app uses [Vite](https://vite.dev/), to install all dependencies from the `frontend/` folder use:

    $ pnpm -i

Then run the frontend for development:

    $ pnpm run dev

or buil the project with:

    $ pnpm run build