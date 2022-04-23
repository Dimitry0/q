import sqlite3 as sql

con = sql.connect('userss.db')

with con:
    db = con.cursor()
    db.execute("""CREATE TABLE IF NOT EXISTS `userss`
        (id INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 0, 
        vk_id STRING,
        clicks INTEGER DEFAULT 0)
        """)
    con.commit()


class UsersInfo:
    def rows():
        db.execute("SELECT COUNT(*) FROM 'userss'")
        con.commit()
        values = db.fetchone()
        return int(values[0])

    def is_reg(user_vk_id):
        db.execute(f"SELECT * FROM 'userss' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        if values is None:
            return False
        else:
            return True

    def insert(user_vk_id):
        db.execute(f"INSERT INTO 'userss' (vk_id) VALUES (?)", (user_vk_id,))
        con.commit()

    def get_clicks(user_vk_id):
        db.execute(f"SELECT clicks FROM 'userss' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        return values[0]

    def update_clicks(user_vk_id, clicks):
        db.execute(f"UPDATE 'userss' SET clicks = {clicks} WHERE vk_id = {user_vk_id}")
        con.commit()

    def get_stavka(user_vk_id):
        db.execute(f"SELECT stavka FROM 'userss' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        return values[0]

    def update_stavka(user_vk_id, stavka):
        db.execute(f"UPDATE 'userss' SET stavka = {stavka} WHERE vk_id = {user_vk_id}")
        con.commit()

    def get_improvements(user_vk_id):
        db.execute(f"SELECT improvements FROM 'userss' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        return values[0]

    def update_improvements(user_vk_id, update):
        db.execute(f"UPDATE 'userss' SET improvements = {update} WHERE vk_id = {user_vk_id}")
        con.commit()

    def get_cars(user_vk_id):
        db.execute(f"SELECT cars FROM 'userss' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        return values[0]

    def update_cars(user_vk_id, update):
        db.execute(f"UPDATE 'userss' SET cars = {update} WHERE vk_id = {user_vk_id}")
        con.commit()

    def get_autosale(user_vk_id):
        db.execute(f"SELECT autosale FROM 'userss' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        return values[0]

    def update_autosale(user_vk_id, update):
        db.execute(f"UPDATE 'userss' SET autosale = {update} WHERE vk_id = {user_vk_id}")
        con.commit()

    def get_cost_or_car(user_vk_id):
        db.execute(f"SELECT cost_of_car FROM 'userss' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        return values[0]

    def update_cost_of_car(user_vk_id, update):
        db.execute(f"UPDATE 'userss' SET cost_of_car = {update} WHERE vk_id = {user_vk_id}")
        con.commit()

    def get_old_car(user_vk_id):
        db.execute(f"SELECT old_car FROM 'userss' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        return values[0]

    def update_old_car(user_vk_id, update):
        db.execute(f"UPDATE 'userss' SET old_car = {update} WHERE vk_id = {user_vk_id}")
        con.commit()

    def get_type_of_car(user_vk_id):
        db.execute(f"SELECT type_of_car FROM 'userss' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        return values[0]

    def update_type_of_car(user_vk_id, update):
        db.execute(f"UPDATE 'userss' SET type_of_car = {update} WHERE vk_id = {user_vk_id}")
        con.commit()

    def get_top(count):
        db.execute(f"SELECT vk_id, clicks FROM 'userss' ORDER BY clicks DESC LIMIT {count}")
        con.commit()
        values = db.fetchall()
        return values

    def get_autosale(count):
        db.execute(f"SELECT vk_id, cars, autosale, cost_of_car FROM 'userss' ORDER BY clicks DESC LIMIT {count}")
        con.commit()
        values = db.fetchall()
        return values

    def get_profile(user_id):
        db.execute(f"SELECT clicks FROM userss WHERE vk_id = {user_id}")
        con.commit()
        value = db.fetchall()
        return value