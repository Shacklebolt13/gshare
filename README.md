# G-SHARE
## How to set up the project ?
1. Clone the repository
2. Install docker and docker compose
3. Add the Environment Variables in a .env file, located at the root of the project.
    Meaning, if your project is at `/app/gshare`, your file would be `app/gshare/.env`

    Defaults are provided here, but they can be tuned as per requirements.

    ```
    #BACKEND APPLICATION SETTINGS
    GSHARE_BE_SECRET_KEY=django_test-insecure
    GSHARE_BE_DEBUG=TRUE
    GSHARE_BE_ALLOWED_HOSTS=localhost,*

    #CELERY WORKER SETTINGS
    CELERY_BROKER_URL=redis://redis:6379
    CELERY_RESULT_BACKEND=redis://redis:6379
    WORKER_LOG_LEVEL=DEBUG

    #DATABASE SETTINGS
    POSTGRES_DB=gshare
    POSTGRES_USER=gshare
    POSTGRES_PASSWORD=gshare
    POSTGRES_PORT=5432
    POSTGRES_DB_HOST=postgres
    ```
4. All done. You have set up the required environment to run the project.

## How to run the Project ?
Run the following command to start the project. `--build` ensures a fresh build of the project if any changes are made to the codebase.

    docker compose up --build

## How to access the project ?
The project can be accessed at `http://localhost/` on your browser.

*but the compose file says 8000, not 80 ?*
<br>The backend is running on port 8000, however, it is being proxied to port 80 by nginx.

*Why nginx ?*
<br>Nginx is used to serve static and media files, as it has inbuilt support for range requests, which makes less work for the backend server.

## *How to run tests ?
To run the tests, you can run the following command.

    docker compose run backend python manage.py test

