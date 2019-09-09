# Snowcrash
Log analyzer and adviser.

# Docker Initialization
`docker build . --tag=snowcrush` <br>
`docker image ls` <br>
`docker run -d snowcrush` <br>
`docker container ls` <br>

#Run without docker
##Install requirement's
 Using `pip install -r requirements.txt`
##Run it
 Using `python main.py --help` 
###Command line options:
`python main.py  --filename PATH          Filename of the log to read from`<br>
`python main.py  --mode [print|lookInDb] print to show Error info, lookInDb to look for data from DB`<br>
`python main.py  --help                   Show this message and exit.`<br>

