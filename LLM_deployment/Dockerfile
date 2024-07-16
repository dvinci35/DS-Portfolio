FROM python:3.10

# Set the work directory in the container
WORKDIR /code

# Copy the requirements file
COPY ./requirements.txt /code/requirements.txt

# Install the requirements as these are not modified often
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Create the environment variables needed
ENV CONFIG_FILE_PATH="/code/app/config.yaml"

# Copy the source code
COPY ./app /code/app

# Expose the port that will be used to post requests
EXPOSE 80

# Instantiate the server when the docker is run
CMD ["uvicorn", "app.server:app", "--port", "80", "--host", "0.0.0.0"]