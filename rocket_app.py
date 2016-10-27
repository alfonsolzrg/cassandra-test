from flask import Flask, flash, jsonify, render_template, redirect, request, session, url_for
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection, ValidationError
from cassandra.cqlengine.management import sync_table

from datetime import datetime
import uuid

from . import models

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

cluster = Cluster()
cass_session = cluster.connect()
keyspace = 'rocket_la_demo'
cass_session.execute('''CREATE KEYSPACE IF NOT EXISTS %s WITH \
  REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1} \
  AND durable_writes = true''' % keyspace)

connection.setup(['127.0.0.1'], "rocket_la_demo", protocol_version=3)
sync_table(models.Activity)
sync_table(models.Questionnaire)

@app.route('/', methods=['GET', 'POST'])
def index():
  """Shows and processes the questionnaire."""
  if request.method == 'GET':
    if not 'user_id' in session:
      session['user_id'] = str(uuid.uuid4())
    return render_template('questionnaire.html')
  else:
    if not 'user_id' in session:
      session['user_id'] = str(uuid.uuid4())
    # Creating a new record in Cassandra, the Object Mapper Way
    try:
      models.Questionnaire.create(
        user_id = session['user_id'],
        name = request.values.get('name', None),
        vim_emacs = request.values.get('vim_emacs', None),
        ide_texteditor = request.values.get('ide_texteditor', None),
        compiled_interpreted = request.values.get('compiled_interpreted', None),
        favorite_ide = request.values.get('favorite_ide', None),
        marry_kiss_kill = {field_name: request.values.get(field_name, None) for \
          field_name in ('marry', 'kiss', 'kill')},
        java_net = request.values.get('java_net', None),
        cloud_providers = request.values.get('cloud_providers', None).split(' '),
        team_size = request.values.get('team_size', None),
        preferred_location = request.values.get('preferred_location', None)
      )
    except ValidationError as e:
      flash(
        'There was an error while processing your answers: %s' % e, 'danger')
      return render_template('questionnaire.html')

    flash("Thank you for your answers! We'll start matching you immediately.",
      'success')
    return redirect(url_for('thanks'))


@app.route('/thanks')
def thanks():
  return render_template('thanks.html')


@app.route('/answers')
def answers():
  """Gets a list of questionnaires answers."""
  # Getting answers from Cassandra, with raw queries
  return render_template('answers.html', 
    questionnaires=models.Questionnaire.objects.all())


@app.route('/feed', methods=['GET', 'POST'])
def feed():
  """Saves a new activity in the feed or shows the complete feed list."""
  if request.method == 'GET':
    feed = cass_session.execute(
      'SELECT user_id, element_name, element_value, change_datetime FROM \
      %s.activity' % keyspace)
    return render_template('feed.html', feed=feed)

  else:
    if not 'user_id' in session:
      session['user_id'] = str(uuid.uuid4())

    element_name = request.values.get('element_name', None)
    element_value = request.values.get('element_value', None)
    if element_name and element_value:
      # Creating a new record in Cassandra, the Prepared Statement way:
      activity_stmt = cass_session.prepare("INSERT INTO %s.activity(id, \
        user_id, element_name, element_value, change_datetime) \
        VALUES(?, ?, ?, ?, ?)" % keyspace)
      cass_session.execute(activity_stmt, [
        uuid.uuid4(),
        uuid.UUID(session['user_id']),
        element_name,
        element_value,
        datetime.now()
      ])

    return jsonify({
      'status': 201,
      'message': 'Created'
    }), 201
