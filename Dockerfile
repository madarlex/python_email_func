FROM python:3.9.13-slim

RUN apt-get update

COPY requirements.txt ./requirements.txt
# Install requirements library
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

# Copy files to docker
COPY . ./

# Add PYTHON PATH environment variable
ENV PYTHONPATH="$PYTHONPATH:/usr/local"

# Make python files executable
RUN chmod +x ./*.py

# Make a link main file
RUN ln -s ./*.py .

# Temp directory to create report files in local to container
RUN mkdir -p /python_email_func/Output
RUN mkdir -p /python_email_func/Customers

ENTRYPOINT ["python"]