import pymysql.cursors

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'db': 'edms',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

st = 0
ed = 3
p = 3