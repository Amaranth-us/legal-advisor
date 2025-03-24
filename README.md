# Project Setup

You can use a virtual environment (venv) to set up the project.

## Virtual Environment (venv)

1. Install Python (3.13.2) for your system: [Official Website](https://www.python.org/downloads/).
    > Ensure that Python is on your `PATH`.
2. Clone the repository to your machine. Navigate to the project directory using the terminal.
    > Ensure that the correct Python interpreter is set for your project environment.
3. Create the virtual environment (only the first time):

    ```bash
    python -m venv .venv
    ```

4. Activate the virtual environment:

    - Windows:

        ```bash
        .venv\Scripts\activate
        ```

    - macOS/Linux:

        ```bash
        source .venv/bin/activate
        ```
        or
        ```bash
        . .venv/bin/activate
        ```

5. Install the dependencies (only the first time):

    ```bash
    pip install -r requirements.txt
    ```

6. Run the FastAPI application:

    ```bash
    cd backend
    python -m uvicorn main:app --reload --port 8001 
    ```
    to run in development mode with the `--reload` flag enabled.

7.  Navigate to [http://127.0.0.1:8081/docs](http://127.0.0.1:8081/docs) to view the API documentation.

8. Run the Streamlit application:

    ```bash
    cd frontend
    streamlit run Home.py
    ```
9. Navigate to [http://127.0.0.1:8501](http://127.0.0.1:8501) to use the application UI.

## Notes
1. Create your own `.env` file in the project directory. The following snxippet shows an example of the file's content with all the necessary variables:

    ```text
    # PostgreSQL configuration
    POSTGRES_USER=db-user
    POSTGRES_PASSWORD=db-password
    POSTGRES_DB=legal-advisor
    POSTGRES_SERVER=postgres
    POSTGRES_PORT=5432

    # FastAPI configuration
    FASTAPI_CODE_PATH=/code
    FASTAPI_VENV_NAME=.venv
    FASTAPI_HOST=0.0.0.0
    FASTAPI_PORT=8081
    ```


### Backend notes

#### PROBLEMS 

My port 8000 is already used by uvicorn:
1.	Find the process using it: lsof -i :8000
And kill it: kill -9 PID
2.	Use another port: uvicorn backend.main:app --reload --port 8001 – this
Use tiktoken for token length and trimming.
Use tencity for hitting API rate limits

Connection issue:
    I created an endpoint for checking the connection and then: curl http://127.0.0.1:8001/test-db-connection

Error: 
Database connection failed: (psycopg2.OperationalError) connection to server at \"localhost\" (127.0.0.1), port 5432 failed: FATAL: password authentication failed for user \"user\"\n\n(Background on this error at: https://sqlalche.me/e/20/e3q8)
Solution:
1.	Open file: sudo nano /Library/PostgreSQL/16/data/pg_hba.conf
2.	Write “trust” for method instead of “scram-sha-256”
3.	Save and exit
4.	Switch to postgres user sudo su – postgres
5.	Stop postgres /Library/PostgreSQL/16/bin/pg_ctl -D /Library/PostgreSQL/16/data stop
6.	Restart postgres /Library/PostgreSQL/16/bin/pg_ctl -D /Library/PostgreSQL/16/data start
Create a requirements.txt : pip freeze > requirements.txt


Manage chat history with PostgreSQL(and SQLAlchemy)

POSTGRES_DATA_PATH=/var/lib/postgresql/data

Create a database

Use pgAdmin4:
1.	Go to Login/Group Roles and select Create > Login/Group Role
    Username: legaladvisoruser
    Password: spqlwmxzpqlQSLlqpW21&
(pswd for superadmin: cwgKT529$)
2.	Create database: legal_advisor
3.	Select database -> properties -> security -> Add new Privilege (ALL privileges)
Run chat-history-init.sql script: 
    $ psql -U legaladvisoruser -d legal_advisor

        Password for user legaladvisoruser: 

legal_advisor$ \i '/Users/one-ai-dev-1/Desktop/untitled folder/projects/inf/legal_advisor/backend/init/chat-history-init.sql'


### Frontend notes
If you want multiple pages, you create a folder named pages in the same directory as main file and inside make the pages with pagename.py etc. 
You can tell it which order to display the pages in, with prefixing the pagenames with a number 1_pagename.py, 2_pagename.py etc.

Frontend is organized in a way that is intuitive to the user. First there is a Home page with basic informayion. Then, on the left side of the screen, there is a navbar with: 
    1. Chat History Page: Shows a list of all sessions, if a user wants to view the history of a specific session; 
    2. Start a New Session Page: Here the user can start a new session, prompt the model (by clicking on the 'Ask' button), get response, and the history of the current session will be shown above the text input field. 





