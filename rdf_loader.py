#!/usr/bin/python3


import logging
import pathlib
from argparse import ArgumentParser

from src import rdf_load


def main():
    parser = ArgumentParser('Load rdf into RedisGraph')
    parser.add_argument('RDF_PATH', help='rdf graph path')
    parser.add_argument('--name', help='graph name', default=None)
    parser.add_argument('--host', help='redis host name', default='localhost')
    parser.add_argument('--port', help='redis port', default=6379)
    parser.add_argument('--format', help='rdf file format', default=None)
    args = parser.parse_args()

    logging.disable(logging.WARNING)

    graph_name = args.graph_name if args.name is not None else pathlib.Path(args.RDF_PATH).name

    rdf_load(args.RDF_PATH, graph_name, args.host, args.port, rdf_format=args.format)


if __name__ == "__main__":
    main()
