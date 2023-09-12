import argparse

from eidos.api.app import run_server

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", help="eidos sub-commands")
subparsers.required = True
subparsers.add_parser("server", help="Deploy server to serve API requests")

args = parser.parse_args()

if args.command == "server":
    run_server()
