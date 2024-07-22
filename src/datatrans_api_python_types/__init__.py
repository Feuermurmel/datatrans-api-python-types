import argparse
import sys
from pathlib import Path

from datatrans_api_python_types.generate import generate


def log(message):
    print(message, file=sys.stderr, flush=True)


class UserError(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("specification_file", type=Path)

    return parser.parse_args()


def entry_point():
    try:
        generate(**vars(parse_args()))
    except UserError as e:
        log(f"error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        log("Operation interrupted.")
        sys.exit(130)
