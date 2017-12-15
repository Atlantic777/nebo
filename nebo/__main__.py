#!/usr/bin/python3
import argparse
import sys

import nebo.handlers as handlers


def setup_argparse():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()
    service_parser = subparsers.add_parser('service')
    run_parser = subparsers.add_parser('run')

    help_msg = "Your python script to run on the EC2 instance."
    service_parser.add_argument('service',
                                metavar='my_script.py',
                                nargs=1,
                                help=help_msg,
                                )
    service_parser.set_defaults(function=handlers.service.service_handler)

    help_msg = "The input file to be processed on the EC2 instance."
    run_parser.add_argument('service',
                            metavar='my_script.py',
                            nargs=1,
                            help=help_msg,
                            )
    run_parser.set_defaults(function=handlers.run.run_handler)
    return parser


def main():
    if len(sys.argv) <= 1:
        sys.argv.append('-h')

    parser = setup_argparse()
    args = parser.parse_args()
    args.function(args)


if __name__ == "__main__":
    main()
