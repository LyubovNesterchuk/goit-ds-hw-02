import sqlite3
from faker import Faker
from random import randint, choice

NUMBER_USERS = 5
NUMBER_TASKS = 2

fake = Faker()


def generate_fake_data(number_users, number_tasks) -> tuple:
    fake_users = [] 
    fake_tasks = []   

    # --- USERS ---
    for _ in range(number_users):
        fake_users.append((fake.name(), fake.unique.email()))

    # --- TASKS (без прив'язки поки) ---
    for _ in range(number_tasks):
        fake_tasks.append((fake.sentence(nb_words=4), fake.text(max_nb_chars=200)))

    return fake_users, fake_tasks


def prepare_data(users, tasks) -> tuple:
    statuses = [('new',), ('in progress',), ('completed',)]

    # --- TASKS з прив'язкою до user_id і status_id ---
    prepared_tasks = []
    for task in tasks:
        title, description = task
        status_id = randint(1, 3)  # 3 статуси
        user_id = randint(1, NUMBER_USERS)

        prepared_tasks.append((title, description, status_id, user_id))

    return users, statuses, prepared_tasks


def insert_data_to_db(users, status, tasks) -> None:
    with sqlite3.connect('tasks.db') as con:
        cur = con.cursor()

        # --- USERS ---
        cur.executemany(
            "INSERT INTO users (fullname, email) VALUES (?, ?)",
            users
        )

        # --- STATUS ---
        cur.executemany(
            "INSERT OR IGNORE INTO status (name) VALUES (?)",
            status
        )

        # --- TASKS ---
        cur.executemany(
            """INSERT INTO tasks (title, description, status_id, user_id)
               VALUES (?, ?, ?, ?)""",
            tasks
        )

        con.commit()


if __name__ == "__main__":
    users, tasks = generate_fake_data(NUMBER_USERS, NUMBER_TASKS)
    users, status, tasks = prepare_data(users, tasks)

    print("USERS:", users)
    print("STATUS:", status)
    print("TASKS:", tasks)

    insert_data_to_db(users, status, tasks)

'''
Після виконання скрипту БД буде заповнена фейковими даними, з якими ми можемо вже працювати та створювати запити.

USERS: [('Gabriella Riley', 'tnash@example.org'), 
('Tyler Johnson', 'lynn90@example.com')]

STATUSES: [('new',), ('in progress',), ('completed',)]

TASKS (first 5): 
[('Adult hard take.', 'Me develop outside page clear admit size church. Treatment thank card sort.\nFinancial able social woman. Pattern its purpose dream.\nStory 
tax trade maybe. Suggest value popular force issue.', 2, 1), 
('Unit kid full some.', 'Your order collection while for. Through walk itself benefit think certainly enough institution.\nUntil society hundred forget meeting. Nothing several grow even property argue baby.', 3, 1)]'''