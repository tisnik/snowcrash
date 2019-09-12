# /usr/bin/env python3
import click
from app import bug_search
from app import language_identity
from app.sql_database import Sql_database


def show_db():
    """Printout all errors in DB"""
    db = Sql_database()
    errors = db.get_errors()
    for error in errors:
        print(
            "Error type: {}, Path: {}, Line: {}, MSG: {}, COUNT: {}, Language: {}, First: {}, Last: {}".format(error[7],
                                                                                                               error[0],
                                                                                                               error[1],
                                                                                                               error[2],
                                                                                                               error[5],
                                                                                                               error[6],
                                                                                                               error[3],
                                                                                                               error[
                                                                                                                   4]))


def get_processed_log(log):
    """Processing log to object"""
    clear_log = bug_search.get_error_from_log(log)
    return language_identity.identify(clear_log)


def print_log(log):
    """Printing processed log"""
    print(get_processed_log(log))


def load_from_file(filename):
    """Loading log from file"""
    data = ""
    with open(filename) as f:
        data = f.read()
        f.close()
    return data


def process_log(log):
    """Processing log and adding to the DB"""
    error = get_processed_log(log)
    db = Sql_database()
    success = db.add_Error(error)
    print(str(error) + ": ", {True: "Success", False: "Failed"}[success])


def add_solution(log, solution, priority, solved):
    log = get_processed_log(log)
    db = Sql_database()
    db.add_solution(type(log).__name__.replace("_error", ""), log.error_type, priority, solution, solved)


@click.command()
@click.option("-f", "--filename", type=click.Path(exists=True), help="Filename of the log to read from")
@click.option("-m", "--mode", required=True, type=click.Choice(['process', 'show_db', 'print', 'add_solution']))
@click.option("-s", "--solution", type=click.STRING, help="The solution")
@click.option("-p", "--priority", type=click.IntRange(0, 999), help="Priority of the solution")
@click.option("-o", "--solved", type=click.BOOL, help="Is solution solved ?")
def main(filename, mode, solution, priority, solved):
    if mode == 'print':
        print_log(load_from_file(filename))
    elif mode == 'show_db':
        show_db()
    elif mode == 'process':
        process_log(load_from_file(filename))
    elif mode == 'add_solution':
        if priority is None or solved is None or solution is None or filename is None:
            print('\033[91m', "Arguments: --priority, --solved, --solution, --filename are required for this mode. ")
            exit(1)
        add_solution(load_from_file(filename), solution, priority, solved)


if __name__ == "__main__":
    main()
