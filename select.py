import sqlite3

DB_NAME = "tasks.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# 1. Завдання певного користувача
def get_tasks_by_user(user_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM tasks WHERE user_id = ?",
            (user_id,)
        ).fetchall()


# 2. Завдання зі статусом 'new'
def get_new_tasks():
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM tasks
            WHERE status_id = (
                SELECT id FROM status WHERE name = 'new'
            )
        """).fetchall()


# 3. Оновити статус завдання на 'in progress'
def update_task_status(task_id):
    with get_connection() as conn:
        conn.execute("""
            UPDATE tasks
            SET status_id = (
                SELECT id FROM status WHERE name = 'in progress'
            )
            WHERE id = ?
        """, (task_id,))
        conn.commit()


# 4. Користувачі без завдань
def get_users_without_tasks():
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM users
            WHERE id NOT IN (
                SELECT DISTINCT user_id FROM tasks
            )
        """).fetchall()


# 5. Додати нове завдання
def add_task(title, description, status_id, user_id):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (?, ?, ?, ?)
        """, (title, description, status_id, user_id))
        conn.commit()


# 6. Завдання, які не завершені
def get_incomplete_tasks():
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM tasks
            WHERE status_id != (
                SELECT id FROM status WHERE name = 'completed'
            )
        """).fetchall()


# 7. Видалити завдання
def delete_task(task_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        conn.commit()


# 8. Користувачі з email через LIKE
def find_users_by_email(pattern):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE email LIKE ?",
            (pattern,)
        ).fetchall()


# 9. Оновити ім’я користувача
def update_user_name(user_id, fullname):
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET fullname = ? WHERE id = ?",
            (fullname, user_id)
        )
        conn.commit()


# 10. Кількість завдань по статусах
def get_task_count_by_status():
    with get_connection() as conn:
        return conn.execute("""
            SELECT s.name, COUNT(t.id) AS task_count
            FROM tasks t
            JOIN status s ON s.id = t.status_id
            GROUP BY s.name
        """).fetchall()


# 11. Завдання користувачів з певним доменом email
def get_tasks_by_email_domain(domain="@example.com"):
    with get_connection() as conn:
        return conn.execute(f"""
            SELECT u.fullname, t.title, t.description
            FROM tasks t
            JOIN users u ON u.id = t.user_id
            WHERE u.email LIKE '%{domain}'
        """).fetchall()


# 12. Завдання без опису
def get_tasks_without_description():
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM tasks
            WHERE description IS NULL OR description = ''
        """).fetchall()


# 13. Користувачі + завдання зі статусом 'in progress'
def get_in_progress_tasks_with_users():
    with get_connection() as conn:
        return conn.execute("""
            SELECT u.fullname, t.title
            FROM users u
            JOIN tasks t ON t.user_id = u.id
            JOIN status s ON s.id = t.status_id
            WHERE s.name = 'in progress'
        """).fetchall()


# 14. Користувачі та кількість їхніх завдань
def get_user_task_counts():
    with get_connection() as conn:
        return conn.execute("""
            SELECT u.fullname, COUNT(t.id) AS task_count
            FROM users u
            LEFT JOIN tasks t ON t.user_id = u.id
            GROUP BY u.id, u.fullname
        """).fetchall()
    

if __name__ == "__main__":
    # 1. Завдання певного користувача
    print("1. Tasks by user:")
    print(get_tasks_by_user(1))

    # 2. Завдання зі статусом 'new'
    print("\n2. New tasks:")
    print(get_new_tasks())

    # 3. Оновити статус завдання
    print("\n3. Update task status:")
    update_task_status(1)
    print("Task 1 updated to 'in progress'")

    # 4. Користувачі без завдань
    print("\n4. Users without tasks:")
    print(get_users_without_tasks())

    # 5. Додати нове завдання
    print("\n5. Add new task:")
    add_task("Test task", "Test description", 1, 1)
    print("New task added")

    # 6. Незавершені завдання
    print("\n6. Incomplete tasks:")
    print(get_incomplete_tasks())

    # 7. Видалити завдання
    print("\n7. Delete task:")
    delete_task(2)
    print("Task 2 deleted")

    # 8. Пошук користувачів по email
    print("\n8. Users by email pattern:")
    print(find_users_by_email("%@example.org"))

    # 9. Оновити ім’я користувача
    print("\n9. Update user name:")
    update_user_name(1, "Updated Name")
    print("User name updated")

    # 10. Кількість завдань по статусах
    print("\n10. Task count by status:")
    print(get_task_count_by_status())

    # 11. Завдання по домену email
    print("\n11. Tasks by email domain:")
    print(get_tasks_by_email_domain("@example.com"))

    # 12. Завдання без опису
    print("\n12. Tasks without description:")
    print(get_tasks_without_description())

    # 13. Завдання 'in progress' з користувачами
    print("\n13. In-progress tasks with users:")
    print(get_in_progress_tasks_with_users())

    # 14. Кількість завдань у користувачів
    print("\n14. User task counts:")
    print(get_user_task_counts())   