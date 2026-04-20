# Отримати всі завдання певного користувача. 
# Використайте SELECT для отримання завдань конкретного користувача за його user_id.

import sqlite3

def execute_query(sql: str, params: tuple = ()) -> list:
    with sqlite3.connect('tasks.db') as con:
        cur = con.cursor()
        cur.execute(sql, params)
        return cur.fetchall()


user_id = 5  

sql = """
SELECT title, description
FROM tasks
WHERE user_id = ?;
"""

'''[('Machine find.', 'From run for control. Debate long fear buy final. Discussion statement represent leave past population team.\nI ground training economic college institution cut. Feel couple specific might bring.'), 
('Measure rate open government.', 'Buy green drive remember bar seem actually. Build baby my hold amount bad education. Including father land company.\nSave leg you nothing. Guess cause six director.')...'''

# sql = """
# SELECT u.fullname, t.title, t.description, s.name
# FROM tasks t
# JOIN users u ON u.id = t.user_id
# JOIN status s ON s.id = t.status_id
# WHERE u.id = ?;
# """

print(execute_query(sql, (user_id,)))


'''[('Steven Velez', 'Seat certain suddenly.', 'Site every join public animal. Risk type mention.', 'completed'), 
('Steven Velez', 'Stop least rather door.', 'Either somebody style rock my happen security.', 'in progress')...]'''

