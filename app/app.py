import os
import flask
from flask import request, jsonify
import sqlalchemy as db

postgres_url = "postgresql://username:secret@db/database"

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['POSTGRES_USER'],
    dbpass=os.environ['POSTGRES_PASSWORD'],
    dbhost='db',
    dbname=os.environ['POSTGRES_DB']
)

engine = db.create_engine(database_uri)

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri


@app.route('/')
def index():
    with engine.connect() as eng:
        rs = eng.execute(
            f"SELECT * FROM data_scientists LIMIT 2")
        num = ""
        for row in rs:
            print(row)
            num = row
        # eng.commit()
    return f'<h1>Sample Docker Flask App</h1><p>Here is the first row of the data_scientists Table: {num}</p>'


@app.route('/api/v1/person/all', methods=['GET'])
def api_all_persons():
    with engine.connect() as eng:
        resultproxy = eng.execute(
            f"SELECT * FROM data_scientists;")
        persons = []
        for rowproxy in resultproxy:
            person = {}
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                if "skill" not in column:
                    person = {**person, **{column: value}}
            persons.append(person)

    return jsonify(persons)


@app.route('/api/v1/person', methods=['GET'])
def api_person_by_id():
    query_parameters = request.args
    id = query_parameters.get('id')
    with engine.connect() as eng:
        person = {}
        person["Skills"] = {}
        resultproxy = eng.execute(
            f"SELECT * FROM data_scientists WHERE user_url='{id}';")
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                if "skill" in column:
                    person["Skills"][column] = value
                else:
                    person[column] = value
        if "id" in person:
            resultproxy = eng.execute(
                f"SELECT * FROM education WHERE scientist_id={person['id']}")
            person["Education"] = []
            for rowproxy in resultproxy:
                education = {}
                # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
                for column, value in rowproxy.items():
                    # build up the dictionary
                    if "scientist_id" not in column:
                        education[column] = value
                person["Education"].append(education)
            resultproxy = eng.execute(
                f"SELECT * FROM education WHERE scientist_id={person['id']}")
            person["Experience"] = []
            for rowproxy in resultproxy:
                experience = {}
                # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
                for column, value in rowproxy.items():
                    # build up the dictionary
                    if "scientist_id" not in column:
                        experience[column] = value
                person["Experience"].append(experience)
        else:
            del person["Skills"]

    return jsonify(person)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)
