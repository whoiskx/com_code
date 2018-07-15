MYSQL_DB = 'nova'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''

sql_drop = """
        DROP TABLE IF EXISTS dd_name;
"""
sql_create = """
                CREATE TABLE `dd_name` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `xs_name` VARCHAR(255) DEFAULT NULL,
                `xs_author` VARCHAR(255) DEFAULT NULL,
                `category` VARCHAR(255) DEFAULT NULL,
                `name_id` VARCHAR(255) DEFAULT NULL,
                PRIMARY KEY (`id`)
)
"""
from pipelines import cur, db

# cur.execute(sql_create)
sql = '''
    SELECT EXISTS (SELECT 1 FROM dd_name WHERE name_id=%(name_id)s)
'''
values = {
    'name_id': 51849
}
cur.execute(sql, values)
cur.fetchall()
for i in cur:
    print(i)