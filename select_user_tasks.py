import sqlite3

def execute_query(sql: str, params: tuple = ()) -> list:
    with sqlite3.connect('tasks.db') as con:
        cur = con.cursor()
        cur.execute(sql, params)
        return cur.fetchall()


user_id = 1  

sql = """
SELECT u.fullname, t.title, t.description, s.name
FROM tasks t
JOIN users u ON u.id = t.user_id
JOIN status s ON s.id = t.status_id
WHERE u.id = ?;
"""

print(execute_query(sql, (user_id,)))

