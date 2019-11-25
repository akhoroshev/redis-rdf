#!/usr/bin/python3

import csv
import datetime
import os
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from typing import List, Tuple, Any

import pandas
import redis
from stringcase import snakecase
from tqdm import tqdm

from src import GpuMemDeltaProfiler, run_command, create_statistic


def parse_result(items: List[Any]) -> List[Tuple[str, Any]]:
    result = list()
    for r in items:
        if isinstance(r, str) and len(r.split(':')) == 2:
            result.append(tuple(r.split(':')))
        elif isinstance(r, list):
            result.append(('checksum', r))
        else:
            # ignoring other types in response
            pass
    return result


def load_suite(path: str) -> List[Tuple[str, str]]:
    result = list()
    with open(path, 'r') as csvfile:
        suite_reader = csv.reader(filter(lambda row: row[0] != '#', csvfile), delimiter=',')
        for row in suite_reader:
            result.append((row[0].strip(), row[1].strip()))
    return result


def main():
    parser = ArgumentParser('Launch test query suit')
    parser.add_argument('TEST_SUIT_PATH', help='test suite in .csv')
    parser.add_argument('--algo', help='algorithms for running', nargs='+', required=True)
    parser.add_argument('--prof', help='memory profiler', default=None)
    parser.add_argument('--pid', help='redis pid', type=int, default=None)
    parser.add_argument('--host', help='redis host name', default='localhost')
    parser.add_argument('--port', help='redis port', default=6379)
    parser.add_argument('--out', help='response output dir path', default='cfpq_results')
    parser.add_argument('--repeat', help='repeat count', type=int, default=5)
    args = parser.parse_args()

    mem_profiler_factory = None
    if args.prof == "gpu":
        mem_profiler_factory = GpuMemDeltaProfiler

    redis_instance = redis.Redis(args.host, args.port)
    suite = load_suite(args.TEST_SUIT_PATH)

    statistic = defaultdict(list)
    try:
        suite_range = tqdm(suite)
        for graph_name, grammar_path in suite_range:
            for algo in args.algo:
                suite_range.set_description(f'Processing {graph_name} {Path(grammar_path).name} {algo}')
                res_repeats = list()
                for _ in tqdm(range(args.repeat), leave=False):
                    res = run_command(redis_instance, ('graph.cfg', algo, graph_name, grammar_path), args.pid,
                                      mem_profiler_factory)
                    res_repeats.append(parse_result(res))
                statistic['graph_name'].append(graph_name)
                statistic['grammar'].append(Path(grammar_path).name)
                statistic['algo'].append(algo)
                for key, value in create_statistic(res_repeats).items():
                    statistic[key].append(value)
    except (KeyboardInterrupt, redis.exceptions.ConnectionError):
        print("Interrupted, saving results...")
    except redis.exceptions.ConnectionError:
        print("Connection error, saving results...")

    path_result = f'{args.out}/{Path(args.TEST_SUIT_PATH).stem}'
    if not os.path.isdir(path_result):
        os.makedirs(path_result)

    df = pandas.DataFrame(statistic)
    df.columns = map(snakecase, df.columns)
    df.to_csv(f"{path_result}/{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')}_stat.csv")


if __name__ == "__main__":
    main()
