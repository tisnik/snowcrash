from app import bug_search, language_identity
from app.sql_database import Sql_database


def show_db():
    """Printout all errors in DB"""
    db = Sql_database()
    errors = db.get_errors()
    text = ""
    for error in errors:
        text += "Error type: {}, Path: {}, Line: {}, MSG: {}, COUNT: {}, Language: {}, First: {}, Last: {}" \
            .format(error[7], error[0], error[1], error[2], error[5], error[6], error[3], error[4])
    return text


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
    return str(error) + ": ", {True: "Success", False: "Failed"}[success]


def add_solution(log, solution, priority, solved):
    log = get_processed_log(log)
    db = Sql_database()
    db.add_solution(type(log).__name__.replace("_error", ""), log.error_type, priority, solution, solved)