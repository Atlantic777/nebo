from nebo.core.client import NeboClient


def run_handler(args, parent_parser):
    client = NeboClient(args.service)
    url = client.send_request(args.input_file, args.args)
    print(url)


def setup_run_parser(run_parser):
    help_msg = "The name of the service to be used."
    run_parser.add_argument('--service',
                            metavar='my-service',
                            type=str,
                            nargs='?',
                            help=help_msg,
                            required=True,
                            )

    help_msg = "The filename to be uploaded and processed."
    run_parser.add_argument('--input-file',
                            metavar='input.txt',
                            type=str,
                            nargs='?',
                            help=help_msg,
                            required=True,
                            )

    run_parser.add_argument('--args',
                            metavar='results.txt',
                            type=str,
                            nargs='?',
                            help=help_msg
                            )

    run_parser.set_defaults(function=run_handler)
