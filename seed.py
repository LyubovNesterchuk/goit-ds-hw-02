import sqlite3
from faker import Faker
from random import randint

NUMBER_USERS = 5
NUMBER_TASKS = 10

fake = Faker()


def generate_fake_data(number_users, number_tasks) -> tuple:
    fake_users = [] 
    fake_tasks = []   

    # --- USERS ---
    for _ in range(number_users):
        fake_users.append((fake.name(), fake.unique.email()))

    # --- TASKS (без прив'язки поки) ---
    for _ in range(number_tasks):
        fake_tasks.append((fake.sentence(nb_words=4), fake.text(max_nb_chars=50)))

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

USERS: [('Shawn Elliott', 'umoore@example.net'), 
('Jill Clark', 'stephaniedavis@example.net'), 
('William Brooks', 'hilldouglas@example.org'), 
('Ryan Lee', 'david14@example.com'), 
('Christopher Larson', 'paigejordan@example.com')] 

STATUS: [('new',), ('in progress',), ('completed',)]

TASKS: [('Compare open those.', 'Keep behind assume protect condition heavy.', 2, 3), 
('Season specific ok increase report.', 'Build rich staff.', 2, 3), 
('Score cause.', 'Around policy yourself strategy.', 3, 2), 
('Office drug enjoy.', 'Serious lay television best.', 2, 1), 
('Trip study.', 'Compare until simple development own.', 1, 2), 
('Official different worker.', 'Should serious quickly start sport sometimes.', 3, 1), 
('Serious amount reach.', 'Set work effect rest maybe. Difficult hot local.', 3, 3), 
('Address far far realize.', 'Identify order central eight weight pass life.', 3, 1), 
('Even adult itself.', 'Team citizen join performance prepare loss.', 1, 2), 
('Show fast every purpose.', 'Think class employee actually cold mother about.', 2, 1)]'''