def run_handler(args):
    print("Hello from the run handler!")

def setup_run_parser(run_parser):
    help_msg = "The input file to be processed on the EC2 instance."
    run_parser.add_argument('service',
                            metavar='my_script.py',
                            nargs=1,
                            help=help_msg,
                            )
    run_parser.set_defaults(function=run_handler)
