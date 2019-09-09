# /usr/bin/env python3
import click
from app import bug_search
from app import language_identity


@click.command()
@click.option("--filename", type=click.STRING, help="Filename of the log to read from")
def main(filename):
    load_from_file(filename)


def process_log(log):
    clear_log = bug_search.get_error_from_log(log)
    error = language_identity.identify(clear_log)
    print(error)


def load_from_file(filename):
    with open(filename) as f:
        process_log(f.read())
        f.close()


if __name__ == "__main__":
    main()
