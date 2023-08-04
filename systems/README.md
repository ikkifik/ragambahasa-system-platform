# Backend—Bhinneka Project (ACE INA I2)

This is a backend side of Bhinneka Project from project code I2-Garuda ACE.

What you will get?

- Basic SQL database migration model.
- Backend API systems for the whole webapps.

### Quick Start
----

**Get the repo**
- [Create new repo](#) from this template
- Clone the repo on GitHub
- … or download .zip from GitHub

**Installation**
- Go to the project directory
- Create new python virtual environment (conda), and activate it

        conda create --name <env_name> python=3.8
        conda activate <env_name>

- Install the required package/library

        pip install -r requirements.txt

**Run the app**
- Define server configuration in `config.py`

        cp config.py.ext config.py
        nano config.py

- Migrate the database

        python migrate.py

- Run Flask application

        python app.py

----
