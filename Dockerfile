# Use an official Python runtime as a parent image
FROM python:3.7

# Set the working directory to /app
WORKDIR /main

# Copy the current directory contents into the container at /app
COPY requirements.txt /main
RUN mkdir /main/tests
COPY tests /main/tests
COPY test.py /main
RUN mkdir /main/app
COPY app/ /main/app

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Define environment variable
ENV NAME snowcrush

# Run app.py when the container launches
CMD ["python3.7", "test.py"]

