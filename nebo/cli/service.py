from nebo.core.service import NeboService
from nebo.aws import S3Handler


def service_handler(args, parser):
    if args.start:
        instance_id = "dummy-instance-id"

        if args.script is None:
            raise ValueError("The --script flag is required to start.")

        if args.name is None:
            raise ValueError("The --name flag is required to start.")

        app_storage = S3Handler(args.name, "apps")
        app_storage.ensure(args.script)

        service = NeboService(script=args.script, init=args.init,
                              name=args.name)
        service.start()
        instance_id = service.instance_id

        if args.quiet:
            print(instance_id)
        else:
            print("Should start instance: ", instance_id)

    elif args.stop:
        if args.instance is None:
            raise ValueError("The --instance flag is required to stop.")

        service = NeboService(instance_id=args.instance)
        service.stop()

    elif args.list:
        pass


def setup_service_parser(service_parser):
    group = service_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--start', action='store_true')
    group.add_argument('--stop', action='store_true')
    group.add_argument('--list', action='store_true')

    help_msg = "Your python script to run on the EC2 instance."
    service_parser.add_argument('--script',
                                metavar='my_script.py',
                                nargs='?',
                                help=help_msg,
                                )

    service_parser.add_argument('--instance',
                                metavar='instance-id',
                                nargs='?',
                                type=str,
                                )

    service_parser.add_argument('--quiet', '-q', action='store_true')
    service_parser.add_argument('--init', '-i', type=str, nargs='?',
                                metavar='init_setup.sh')

    service_parser.add_argument('--name', '-n', type=str, metavar='my-service')

    service_parser.set_defaults(function=service_handler)
