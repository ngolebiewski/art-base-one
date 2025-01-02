DB App for Professional Visual Artists.

Dev log:
1. Set up git + repo
2. Make Virtual Environment
    a. `python3 -m venv venv`
    b. `source venv/bin/activate`
    c. Deactivate with: `deactivate`
3. Export SQLITE Database schema
    ```
    .output schema.sql
    .schema
    .output stdout
    ```
4. Connect to db, autogenerate models.py from schema written for sqlite db. Using 'artbasetwo.db'
5. Figuring out FastAPI

