from statistics import mean
from tqdm import tqdm

from mem_prof import MemDeltaProfiler
from cfpq_query import cfpq_query


ALGO_LIST = ['cpu1', 'cpu3']
MEM_INTERVAL_COUNT = 20


def get_grammar_file(grammar_path):
    return grammar_path.split('/')[-1]


def test_performance_on_graph(graph_name, grammar_path, redis_instance, redis_pid, exec_count=1):
    result = {
        algo: {
            column: []
            for column in ['iterations', 'control_sum', 'time', 'mem']
        } for algo in ALGO_LIST
    }

    for algo in ALGO_LIST:
        # Get approximately query time
        exec_time = cfpq_query(algo, graph_name, grammar_path, redis_instance).time * 1.5
        # exec_time = 1

        # Run exec_count times algorithm
        for _ in tqdm(range(exec_count)):
            mem_prof = MemDeltaProfiler()
            mem_prof.start(redis_pid, exec_time / MEM_INTERVAL_COUNT, exec_time)
            resp = cfpq_query(algo, graph_name, grammar_path, redis_instance)
            max_mem = mem_prof.end()

            result[algo]['iterations'].append(resp.iterations)
            result[algo]['control_sum'].append(resp.control_sums)
            result[algo]['time'].append(resp.time)
            result[algo]['mem'].append(max_mem)
    return result


def test_performance_on_suite(test_suite, redis_instance, redis_pid, execute_count=10, statistics=(mean, min, max)):
    full_results = {
        'graph': [],
        'grammar': []
    }

    statistics_results = {
        'graph': [],
        'grammar': []
    }

    for graph_name, grammar_path in tqdm(test_suite):
        res_test = test_performance_on_graph(graph_name, grammar_path, redis_instance, redis_pid, execute_count)

        full_results['graph'].extend([graph_name] * execute_count)
        full_results['grammar'].extend([get_grammar_file(grammar_path)] * execute_count)

        statistics_results['graph'].append(graph_name)
        statistics_results['grammar'].append(get_grammar_file(grammar_path))

        for algo, execute_info in res_test.items():
            # Write total results
            for column, values in execute_info.items():
                key = f'{column}_{algo}'
                full_results.setdefault(key, [])
                full_results[key].extend(values)

            # Write statistics
            for column in ['control_sum', 'iterations']:
                first_value = execute_info[column][0]
                assert all(x == first_value for x in execute_info[column])

                key = f'{column}_{algo}'
                statistics_results.setdefault(key, [])
                statistics_results[key].append(first_value)

            for column in ['time', 'mem']:
                for statistic in statistics:
                    key = f'{column}_{statistic.__name__}_{algo}'
                    statistics_results.setdefault(key, [])
                    statistics_results[key].append(statistic(execute_info[column]))

    return full_results, statistics_results


# SF_GRAMMAR_PATH = '/home/simleton/Repo/redis-rdf/src/graph_gen/grammars/an_bm_cm_dn.txt'
# NEO4J = [
#     ('directed_free_scale_net_500_10.txt',  SF_GRAMMAR_PATH),
# ]
#
#
# xs = test_performance_on_suite(NEO4J, 2)
# print(xs[1])
