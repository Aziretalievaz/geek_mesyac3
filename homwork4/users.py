
from database import get_db
from queries import (
    GET_USER_BY_TG_ID,
    INSERT_USER,
    UPDATE_USER_USERNAME, 
    DELETE_USER
)

def update_user(telegram_id: int, username: str):
    conn = get_db()
    conn.execute(UPDATE_USER_USERNAME, (username, telegram_id))
    conn.commit()
    conn.close()


def delete_user(telegram_id: int):
    conn = get_db()
    conn.execute(DELETE_USER, (telegram_id,))
    conn.commit()
    conn.close()


def get_user(telegram_id: int):
    conn = get_db()
    user = conn.execute(GET_USER_BY_TG_ID, (telegram_id,)).fetchone()
    conn.close()
    return user


def create_user(telegram_id: int, username: str):
    conn = get_db()
    conn.execute(INSERT_USER, (telegram_id, username))
    conn.commit()
    conn.close()
    return get_user(telegram_id)