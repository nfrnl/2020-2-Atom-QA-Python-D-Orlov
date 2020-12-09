import sqlalchemy
from sqlalchemy.orm import sessionmaker


class MySQLConnectionORM:
    def __init__(self, user, password, db_name, host='127.0.0.1', port=3306):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.host = host
        self.port = port

        self.connection = self.connect()
        session = sessionmaker(bind=self.connection)
        self.session = session()

    def get_connection(self, db_created=False):
        engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name if db_created else ""}'
        )
        return engine.connect()

    def connect(self):
        connection = self.get_connection(db_created=False)

        connection.execute(f'DROP DATABASE IF EXISTS {self.db_name}')
        connection.execute(f'CREATE DATABASE {self.db_name}')
        connection.close()

        return self.get_connection(db_created=True)
