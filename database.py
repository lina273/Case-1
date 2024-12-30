from tinydb import TinyDB, Query

db = TinyDB('database.json')
User = Query()
db.insert({'name': 'John', 'age': 22})
db.search(User.name == 'John')
[{'name': 'John', 'age': 22}]