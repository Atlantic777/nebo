from ..client import NeboClient


def run_handler(args, parent_parser):
    client = NeboClient(args.service)
    client.send_request(args.input_file, args.output_file, args.args)

    with open(args.output_file) as f:
        print(f.read())

    print("Done!")


def setup_run_parser(run_parser):
    help_msg = "The name of the service to be used."
    run_parser.add_argument('--service',
                            metavar='my-service',
                            type=str,
                            nargs='?',
                            help=help_msg,
                            )

    help_msg = "The filename to be uploaded and processed."
    run_parser.add_argument('--input-file',
                            metavar='input.txt',
                            type=str,
                            nargs='?',
                            help=help_msg,
                            )

    help_msg = "The filename where to store the result."
    run_parser.add_argument('--output-file',
                            metavar='results.txt',
                            type=str,
                            nargs='?',
                            help=help_msg
                            )

    run_parser.add_argument('--args',
                            metavar='results.txt',
                            type=str,
                            nargs='?',
                            help=help_msg
                            )

    run_parser.set_defaults(function=run_handler)
