from faker import Faker

from db_client.client import MySQLConnection
from db_client.orm_client import MySQLConnectionORM
from models.models import Base, User

fake = Faker()


class MySQLBuilder:
    def __init__(self, connection: MySQLConnection):
        self.connection = connection

        self.create_users()

    def create_users(self):
        users_create_query = '''
            CREATE TABLE IF NOT EXISTS `users` (
                `id` SMALLINT(6) NOT NULL AUTO_INCREMENT,
                `username` CHAR(20) NOT NULL,
                `email` CHAR(30) NOT NULL,
                `name` CHAR(60) NOT NULL,
                `birthday` DATE,
                `is_male` BOOLEAN,
                `about_text` TEXT,
                PRIMARY KEY (`id`)
            ) CHARSET=utf8
        '''
        self.connection.execute_query(users_create_query)

    def add_user(self):
        fake_profile = fake.simple_profile()
        fake_info = fake.sentence()
        add_user_query = f"INSERT INTO users(username, email, name, birthday, is_male, about_text)" \
                         f"VALUES('{fake_profile['username']}', '{fake_profile['mail']}', '{fake_profile['name']}', " \
                         f"'{fake_profile['birthdate']}', '{1 if fake_profile['sex'] == 'M' else 0}', " \
                         f"'{fake_info}')"
        self.connection.execute_query(add_user_query)
        return {'username': fake_profile['username'],
                'email': fake_profile['mail'],
                'name': fake_profile['name'],
                'birthday': fake_profile['birthdate'],
                'is_male': True if fake_profile['sex'] == 'M' else False,
                'about_text': fake_info}


class MySQLBuilderORM:
    def __init__(self, connection: MySQLConnectionORM):
        self.connection = connection
        self.engine = self.connection.connection.engine

        self.create_users()

    def create_users(self):
        if not self.engine.dialect.has_table(self.engine, 'users'):
            Base.metadata.tables['users'].create(self.engine)

    def add_user(self):
        fake_profile = fake.simple_profile()
        user = User(
            username=fake_profile['username'],
            email=fake_profile['mail'],
            name=fake_profile['name'],
            birthday=fake_profile['birthdate'],
            is_male=True if fake_profile['sex'] == 'M' else False,
            about_text=fake.sentence()
        )
        self.connection.session.add(user)
        self.connection.session.commit()
        return user
