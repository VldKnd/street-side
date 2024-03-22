import argparse

import uvicorn


def parse_command() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=('Starts a web server that serves a REST API for the Street Side project.'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '--host',
        help='The host to bind to.',
        type=str,
        default="0.0.0.0",
    )
    parser.add_argument(
        '--port',
        help='The port to bind to.',
        type=int,
        default=8080,
    )

    # argparse does not convert to bool, see,
    # https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    parser.add_argument(
        '--reload',
        help='Enable auto-reload of the server.',
        type=str,
        choices=["true", "false"],
        default="false",
    )

    parser.add_argument(
        '--workers',
        help='The number of workers to use. Incompatible with --reload.',
        type=int,
        default=1,
    )

    parser.add_argument(
        '--log-config',
        help='The JSON log config file to configure logging.',
        type=str,
        default="log_config.json",
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_command()
    uvicorn.run(
        "street_side_api.app.factory:app",
        log_config=args.log_config,
        reload=True if args.reload == "true" else False,
        log_level="info",
        host=args.host,
        port=args.port,
        workers=args.workers if args.reload == "false" else 1,
        headers=[
            ('Connection', 'close'),
        ],
    )
