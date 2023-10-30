# Game Zone API
Welcome to Game Zone Project! This project is set up with Django, Poetry, Docker, and Docker Compose to make installation and local development a breeze.

We are build open source GraphQl API for gaming platform.
Our goal to make great gaming platform and have big community.

## Prerequisites

Before you get started, ensure you have the following installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.10 or higher: [Python Installation](https://www.python.org/downloads/)
- Poetry: [Install Poetry](https://python-poetry.org/docs/)
- Strawberry GraphQL: [Install Strawberry](https://strawberry.rocks/docs/getting-started)

## Quick Start

1. **Clone the repository:**

   ```bash
   git clone git@github.com:VachaganGrigoryan/gamezone-app.git
   cd gamezone-app
   ```
2. Clone `.env.example` file to `.env` file and change variables.
   ```bash
    cp .env.example .env
    ```
3. **Start the Docker containers:**

    ```bash
    docker-compose up --build
    ```

## Installation

1. **Create a virtual environment using Poetry:**

   ```bash
   poetry install
   ```

2. **Start the Docker containers:**

    ```bash
    docker-compose up --build
    ```
3. **Apply database migrations:**

    ```bash
    docker-compose exec api python manage.py migrate
    ```
4. **Create a superuser:**

    ```bash
    docker-compose exec api python manage.py createsuperuser
    ```
5. **Access the Django development server:**
   - Django Admin: http://127.0.0.1:8000/admin/
   - GraphQl Playground: http://127.0.0.1:8000/graphql/

## Docker and Docker Compose
- The Docker containers are defined in the `docker-compose.yml` file.
- The Docker Compose configuration is set up to use the `.env` file for environment variables.
- Edit dockerfile and docker-compose.yml files to change the configuration of the containers.

## Project Structure
- `account/`: Django app for user authentication.
- `core/`: Django app for core functionality of the project.
- `game/`: Django app for game, here we can new game as django app.
- `server/`: Django project settings.
- `scripts/`: Scripts for development and production.

## Development and Deployment
Adjust settings in the `.env` file for development and production.
For production deployment, consider additional configuration, such as using a production-ready database and web server.
