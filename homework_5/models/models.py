from sqlalchemy import Column, Integer, String, Date, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    email = Column(String(30), nullable=False)
    name = Column(String(60), nullable=False)
    birthday = Column(Date)
    is_male = Column(Boolean)
    about_text = Column(Text)

    def __repr__(self):
        return f"<User(id='{self.id}', nickname='{self.username}', name='{self.name}', email='{self.email}')>"


class QueryAmount(Base):
    __tablename__ = 'query_amount'

    method = Column(String(15), primary_key=True)
    amount = Column(Integer, nullable=False)


class LargestQuery(Base):
    __tablename__ = 'largest_queries'

    id = Column(Integer, primary_key=True)
    url = Column(String(2000), nullable=False)
    status_code = Column(Integer)
    bytes_sent = Column(Integer)
    count = Column(Integer, nullable=False)


class FrequentClientError(Base):
    __tablename__ = 'frequent_client_errors'

    id = Column(Integer, primary_key=True)
    url = Column(String(2000), nullable=False)
    status_code = Column(Integer, nullable=False)
    ip = Column(String(15), nullable=False)


class LargestServerError(Base):
    __tablename__ = 'largest_server_errors'

    id = Column(Integer, primary_key=True)
    url = Column(String(2000), nullable=False)
    status_code = Column(Integer, nullable=False)
    ip = Column(String(15), nullable=False)
