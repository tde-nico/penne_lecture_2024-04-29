import sqlite3

def create_db():
    with open('quiz.db', 'w') as f:
        pass

    conn = sqlite3.connect('quiz.db')

    c = conn.cursor()
    
    # Create users table if not exists
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            current_score INTEGER DEFAULT 0,
            admin INTEGER DEFAULT 0
        )
    ''')
    
    # Create questions table if not exists
    c.execute('''
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            choices TEXT NOT NULL,  -- This will store choices as a comma-separated string
            answer TEXT NOT NULL,
            show INTEGER DEFAULT 0,
            timestamp INTEGER DEFAULT 0
        )
    ''')
    
    # Create scores table if not exists
    c.execute('''
        CREATE TABLE scores (
            user_id INTEGER,
            score INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    

    # submission
    c.execute('''
        CREATE TABLE submission (
            user_id INTEGER,
            question_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(question_id) REFERENCES questions(id)
        )
    ''')

    # Insert example questions (check if they are already there to avoid duplicates)
    

    import time
    from domande import questions
    domanda_di_prova = {
        'question': 'Qual è il tuo nome?',
        'answers': [
            'Mi chiamo Mario',
            'Il mio nome è Luigi',
            'Mi chiamo Paperino',
            'Il mio nome è Topolino'
        ],
        'correct': 'Mi chiamo Mario'
    }
    from random import sample
    
    c.execute('INSERT INTO questions (question, choices, answer, show, timestamp) VALUES (?,?,?,?,?)', (domanda_di_prova['question'], ','.join(domanda_di_prova['answers']), domanda_di_prova['correct'], 1, int(time.time()) - 1000,)) 

    for q in questions:
        c.execute('INSERT INTO questions (question, choices, answer) VALUES (?, ?, ?)', (q["question"], ','.join(sample(q['answers'], len(q['answers']))), q["correct"], ))

    admin_acc = ('admin', 'EmilioCoppa31415', 2000000000, 1)
    c.execute('INSERT INTO users (username, password, current_score, admin) VALUES (?, ?, ?, ?)', admin_acc)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
