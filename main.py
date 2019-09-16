# /usr/bin/env python3
import click
from app.controler import show_db, print_log, load_from_file, process_log, add_solution
from app.gui import Gui


@click.command()
@click.option("-f", "--filename", type=click.Path(exists=True), help="Filename of the log to read from")
@click.option("-m", "--mode", type=click.Choice(['process', 'show_db', 'print', 'add_solution', 'gui']))
@click.option("-s", "--solution", type=click.STRING, help="The solution")
@click.option("-p", "--priority", type=click.IntRange(0, 999), help="Priority of the solution")
@click.option("-o", "--solved", type=click.BOOL, help="Is solution solved ?")
def main(filename, mode, solution, priority, solved):
    if mode == 'print':
        print_log(load_from_file(filename))
    elif mode == 'show_db':
        print(show_db())
    elif mode == 'process':
        print(process_log(load_from_file(filename)))
    elif mode == 'add_solution':
        if priority is None or solved is None or solution is None or filename is None:
            print('\033[91m',
                  "Arguments: --priority, --solved, --solution, --filename are required for this mode. ")
            exit(1)
        add_solution(load_from_file(filename), solution, priority, solved)
    else:
        Gui()


if __name__ == "__main__":
    main()
