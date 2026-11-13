import sqlite3

from queries import (
    CREATE_USERS_TABLE,
    CREATE_QUESTIONS_TABLE,
    CREATE_RESULTS_TABLE,
    GET_ALL_QUESTIONS,
    INSERT_QUESTION
)
from questions import QUESTIONS
from config import DATABASE



def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute(CREATE_USERS_TABLE)
    conn.execute(CREATE_QUESTIONS_TABLE)
    conn.execute(CREATE_RESULTS_TABLE)


# Заполняем вопросы если таблица пустая
    
    if not conn.execute(GET_ALL_QUESTIONS).fetchall():
        for q_text, q_answer in QUESTIONS:
            conn.execute(INSERT_QUESTION, (q_text, q_answer))


    conn.commit()
    conn.close()

