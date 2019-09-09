# /usr/bin/env python3
import click
from app import bug_search
from app import language_identity


def look_in_db(filename):
    pass


def process_log(log):
    clear_log = bug_search.get_error_from_log(log)
    error = language_identity.identify(clear_log)
    print(error)


def load_from_file(filename):
    with open(filename) as f:
        process_log(f.read())
        f.close()


@click.command()
@click.option("--filename", type=click.Path(exists=True), help="Filename of the log to read from")
@click.option("--mode", type=click.Choice(['print', 'lookInDb']))
def main(filename, mode):
    if mode == 'print':
        load_from_file(filename)
    elif mode == 'lookInDb':
        look_in_db(filename)


if __name__ == "__main__":
    main()
