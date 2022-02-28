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


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/')
def index():
    with engine.connect() as eng:
        rs = eng.execute(
            f"SELECT * FROM american_football_action_participants LIMIT 10")
        num = ""
        for row in rs:
            print(row)
            num = row
        # eng.commit()
    return f'<h1>Distant Reading Archive</h1><p>A prototype API for distant reading of science fiction novels, selected {num} rows</p>'


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


""" 


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)
 """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)
