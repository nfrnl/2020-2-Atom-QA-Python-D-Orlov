import argparse
from collections import Counter
import itertools
import re
import sys

from db_client.orm_client import MySQLConnectionORM
from models.models import Base, QueryAmount, LargestQuery, FrequentClientError, LargestServerError


def queries_num_by_method(queries):
    result = {}
    method_pattern = re.compile(r'.* \"([A-Z]+) .*')
    for query in queries:
        if method_pattern.match(query) is None:
            continue
        match = method_pattern.match(query).group(1)
        if match in result:
            result[match] += 1
        else:
            result[match] = 1
    return result


def largest_queries(queries):
    temp_list = []
    for query in queries:
        split_query = query.split()
        bytes_sent = split_query[9]
        if bytes_sent.isnumeric():
            temp_list.append((split_query[5], split_query[6], split_query[7], split_query[8], bytes_sent))
    sort_res = sorted(temp_list, key=lambda item: int(item[4]))
    uniq_res = [(g[0][1], g[0][3], g[0][4], len(list(g[1]))) for g in itertools.groupby(sort_res)][-10:]
    return list(reversed(uniq_res))


def most_frequent_client_errors(queries):
    temp_list = []
    for query in queries:
        split_query = query.split()
        if split_query[8].startswith('4'):
            temp_list.append((split_query[0], split_query[6], split_query[8]))
    sort_res = Counter(temp_list).most_common(10)
    return [(res[0][1], res[0][2], res[0][0]) for res in sort_res]


def largest_server_errors(queries):
    temp_list = []
    for query in queries:
        split_query = query.split()
        if split_query[8].startswith('5'):
            temp_list.append((split_query[0], split_query[6], split_query[8], split_query[9]))
    sort_res = sorted(temp_list, key=lambda item: int(item[3]))[-10:]
    return [(res[1], res[2], res[0]) for res in reversed(sort_res)]


def write_data_to_db(log_lines, user, password, db_name, host, port):
    connection = MySQLConnectionORM(user, password, db_name, host, port)
    engine = connection.connection.engine
    for model in (QueryAmount, LargestQuery, FrequentClientError, LargestServerError):
        if not engine.dialect.has_table(engine, model.__tablename__):
            Base.metadata.tables[model.__tablename__].create(engine)
        else:
            connection.session.query(model).delete()
    connection.session.commit()
    for method_stats in sorted(queries_num_by_method(log_lines).items()):
        connection.session.add(QueryAmount(method=method_stats[0], amount=int(method_stats[1])))
    for line in largest_queries(log_lines):
        connection.session.add(LargestQuery(url=line[0], status_code=line[1], bytes_sent=line[2], count=line[3]))
    for line in most_frequent_client_errors(log_lines):
        connection.session.add(FrequentClientError(url=line[0], status_code=line[1], ip=line[2]))
    for line in largest_server_errors(log_lines):
        connection.session.add(LargestServerError(url=line[0], status_code=line[1], ip=line[2]))
    connection.session.commit()


parser = argparse.ArgumentParser()
parser.add_argument('input_filename')
parser.add_argument('--user', default='root')
parser.add_argument('--password', default='dbpass')
parser.add_argument('--db', default='log_stats')
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', default=3306)
args = parser.parse_args()

pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} ')

with open(args.input_filename) as in_file:
    file_lines = in_file.readlines()
    valid_lines = [line.rstrip() for line in file_lines if pattern.match(line)]
    if len(valid_lines) == 0:
        print('Error: no valid entries found', file=sys.stderr)
        exit(1)
    write_data_to_db(valid_lines, args.user, args.password, args.db, args.host, int(args.port))
