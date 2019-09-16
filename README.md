# Snowcrash
Log analyzer and adviser.

# Docker Initialization
Install `docker-compose`<br>
Using `docker-compose up`

# Run without docker
## Install requirement's
 Using `pip install -r requirements.txt`
## If you want to run GUI
### You need to install Tkinter
#### Windows
If you have installed python you have tkinter by default.
#### RPM package manager
 `sudo dnf update && sudo dnf install python3-tkinter`
#### APT package manager
`sudo apt-get update && sudo apt-get install python3-tk`
## Run it
 Using `python main.py --help` 
### Command line options:
`-f, --filename PATH             Filename of the log to read from` <br>
`-m, --mode [process|show_db|print] Select mode` <br>
`-s, --solution TEXT             The solution`<br>
`-p, --priority INTEGER RANGE    Priority of the solution`<br>
`-o, --solved BOOLEAN            Is solution solved ?`<br>
`--help                          Show this message and exit.`<br>
