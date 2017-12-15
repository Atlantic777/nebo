#!/usr/bin/python3
import argparse
import sys

import nebo.handlers


def setup_argparse():
    parser = argparse.ArgumentParser("nebo")

    subparsers = parser.add_subparsers()
    service_parser = subparsers.add_parser('service')
    run_parser = subparsers.add_parser('run')

    nebo.handlers.service.setup_service_parser(service_parser)
    nebo.handlers.run.setup_run_parser(run_parser)

    return parser


def main():
    if len(sys.argv) <= 1:
        sys.argv.append('-h')

    parser = setup_argparse()
    args = parser.parse_args()

    try:
        args.function(args, parser)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
