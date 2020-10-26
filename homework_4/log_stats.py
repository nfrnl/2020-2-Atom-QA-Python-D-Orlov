import argparse
from collections import Counter
import itertools
import json
import re
import sys


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


def get_json_data(log_lines):
    return {'Total queries': len(log_lines),
            'Requests by method': queries_num_by_method(log_lines),
            'Largest requests by bytes sent': largest_queries(log_lines),
            'Most frequent requests with server error response': largest_queries(log_lines),
            'Largest requests by bytes sent with server error response': largest_server_errors(log_lines)}


def write_data(log_lines, out_file, is_json):
    if out_file is None:
        if is_json:
            data = get_json_data(log_lines)
            print(json.dumps(data, indent=4))
        else:
            print('Total queries:', len(log_lines))
            print('--------')
            for method_stats in sorted(queries_num_by_method(log_lines).items()):
                print(method_stats[0], '-', method_stats[1])
            print('--------')
            for line in largest_queries(log_lines):
                print(*line)
            print('--------')
            for line in most_frequent_client_errors(log_lines):
                print(*line)
            print('--------')
            for line in largest_server_errors(log_lines):
                print(*line)
            print('--------')
    else:
        with open(out_file, 'a') as file:
            if is_json:
                data = get_json_data(log_lines)
                json.dump(data, file)
                file.write('\n')
            else:
                file.write('Total queries:' + str(len(log_lines)) + '\n')
                file.write('--------\n')
                for method_stats in sorted(queries_num_by_method(log_lines).items()):
                    file.write(method_stats[0] + ' - ' + str(method_stats[1]) + '\n')
                file.write('--------\n')
                for line in largest_queries(log_lines):
                    file.write(' '.join(str(col) for col in line) + '\n')
                file.write('--------\n')
                for line in most_frequent_client_errors(log_lines):
                    file.write(' '.join(str(col) for col in line) + '\n')
                file.write('--------\n')
                for line in largest_server_errors(log_lines):
                    file.write(' '.join(str(col) for col in line) + '\n')
                file.write('--------\n')


parser = argparse.ArgumentParser()
parser.add_argument('input_filename')
parser.add_argument('output_filename', nargs='?', default=None)
parser.add_argument('--json', action='store_true')
args = parser.parse_args()

pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} ')

with open(args.input_filename) as in_file:
    file_lines = in_file.readlines()
    valid_lines = [line.rstrip() for line in file_lines if pattern.match(line)]
    if len(valid_lines) == 0:
        print('Error: no valid entries found', file=sys.stderr)
        exit(1)
    write_data(valid_lines, args.output_filename, args.json)
