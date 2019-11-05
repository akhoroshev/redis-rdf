from redis import Redis

COMMON_CMD = 'graph.cfg'


def _get_iterations(resp):
    return resp[1].split()[-1]


def _get_control_sums(resp):
    return ', '.join(resp[2:])


def _get_time(resp):
    return float(resp[0].split()[-1])


class CfpqResponse:
    def __init__(self, time, iterations, control_sums):
        self.time = time
        self.iterations = iterations
        self.control_sums = control_sums


def cfpq_query(algo: str, graph_name: str, grammar_path: str, redis: Redis):
    resp = [s.decode('UTF-8') for s in redis.execute_command(COMMON_CMD, algo, graph_name, grammar_path)]
    return CfpqResponse(_get_time(resp), _get_iterations(resp), _get_control_sums(resp))
