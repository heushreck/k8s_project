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
            f"SELECT * FROM american_football_action_participants LIMIT 1")
        num = ""
        for row in rs:
            print(row)
            num = row
        # eng.commit()
    return f'<h1>Sample Docker Flask App</h1><p>Here is the first row of the american_football_action_participants Table: {num}</p>'


@app.route('/api/v1/all/events', methods=['GET'])
def api_event_by_id():
    query_parameters = request.args
    id = query_parameters.get('id')
    with engine.connect() as eng:
        resultproxy = eng.execute(
            f"SELECT * FROM events WHERE id={id}")
        player = {}
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                player = {**player, **{column: value}}

    return jsonify(player)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)
