from fastapi import FastAPI

app = FastAPI()

config = [
    {
        'name': 'workstation',
        'ethaddr': '24:4b:fe:df:d0:f6',
        'hostname': 'fractal-i7',
        'ssh_username': 'stefan.golinschi',
        'ssh_port': 22, 'enabled': True
    },
    {
        'name': 'fractal-i2',
        'ethaddr': '00:11:22:33:44:55',
        'hostname': 'xsvm.eu',
        'ssh_username': 'root',
        'ssh_port': 22,
        'enabled': False
    }
]


def main():
    create_logger()

    args = argument_parser()
    config_file = args.config

    if not valid_config(config_file):
        exit(1)

    config = load_config(config_file)['endpoints']

    print(config)

    endpoints = []

    for item in config:
        settings = item

        ep = Endpoint(settings)
        endpoints.append(ep)

        print(f"{ep.name}: {ep.wake()}")

    app = FastAPI()


if __name__ == "__main__":
    main()
