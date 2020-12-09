import pytest

from db_client.client import MySQLConnection
from db_client.orm_client import MySQLConnectionORM
from models.models import User
from tests.builder import MySQLBuilder, MySQLBuilderORM


@pytest.fixture(scope='session')
def mysql_client():
    return MySQLConnection(user='root', password='dbpass', db_name='test_python')


@pytest.fixture(scope='session')
def mysql_client_orm():
    return MySQLConnectionORM(user='root', password='dbpass', db_name='test_python_orm')


class TestMySQL:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql = mysql_client
        self.builder = MySQLBuilder(connection=self.mysql)

    def test_database(self):
        user = self.builder.add_user()
        query_res = self.mysql.execute_query('SELECT * FROM users ORDER BY id DESC LIMIT 1')
        assert query_res[0]['email'] == user['email']


class TestMySQLORM:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client_orm):
        self.mysql = mysql_client_orm
        self.builder = MySQLBuilderORM(connection=self.mysql)

    def test_database_orm(self):
        user = self.builder.add_user()
        query_res = self.mysql.session.query(User).order_by(User.id.desc()).first()
        assert query_res.email == user.email
