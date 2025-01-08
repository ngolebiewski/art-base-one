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
5. Figuring out FastAPI...(ongoing)
6. Update schema, then update models.py --> reverse of how it should be done, but I feel invested in the schema as it stands -- along with the view. Will swap to model as primary source once switching databses to PostgreSQL


## TODO:
- Python script to import CSV of artworks.
- Avoid duplication of artworks