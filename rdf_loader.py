#!/usr/bin/python3


import logging
from argparse import ArgumentParser

from src import rdf_load


def main():
    parser = ArgumentParser('Load rdf into RedisGraph')
    parser.add_argument('RDF_PATH', help='rdf graph path')
    parser.add_argument('GRAPH_NAME', help='redis graph name')
    parser.add_argument('--host', help='redis host name', default='localhost')
    parser.add_argument('--port', help='redis port', default=6379)
    args = parser.parse_args()

    logging.disable(logging.WARNING)

    rdf_load(args.RDF_PATH, args.GRAPH_NAME, args.host, args.port)


if __name__ == "__main__":
    main()
