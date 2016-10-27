# Sample project to learn Flask, VueJS & Apache Cassandra.

## Install instructions

- Make sure you have Python 2.7.X
- Make sure you have your Python version's development headers
- Create a virtualenv (`virtualenv env_name`)
- Install dependencies `pip install -r requirements.txt`
- Run the following commands:
    - `export FLASK_APP=rocket_app.py`
    - `export FLASK_DEBUG=1` (optional, if you wish to debug)
- Run the app: `flask run`

On the first run it will connect to a Cassandra cluster on localhost and create a new Keyspace with the name `rocket_la_demo`, then proceed to create two tables: `Activity` and `Questionnaire`.

Once the last command fires up the development server, go to [http://localhost:5000/](http://localhost:5000/)