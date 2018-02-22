#!/usr/bin/env python3

import argparse
import multiprocessing
import traceback
import urllib.request


def get_number(url):
    with urllib.request.urlopen(url) as response:
        return int(response.read().decode('utf-8'))


def get_numbers(args):
    task_id, url, num_requests = args
    response_set = set()
    try:
        for i in range(num_requests):
            value = get_number(url)
            print('task', task_id, 'received', value)
            response_set.add(value)
    except Exception:
        traceback.print_exc()
    return response_set


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-j', '--parallel', default=4, type=int)
    parser.add_argument('-n', '--request', default=100, type=int)
    args = parser.parse_args()

    tasks = [(i, args.url, args.request) for i in range(args.parallel)]

    with multiprocessing.Pool(processes=args.parallel) as pool:
        response_sets = pool.map(get_numbers, tasks)

    answer = set()
    for i, response_set in enumerate(response_sets):
        print('task', i, 'received', len(response_set), 'numbers')
        answer.update(response_set)

    print('total', len(answer))

    print('last extra request got:', get_number(args.url))

if __name__ == '__main__':
    main()
