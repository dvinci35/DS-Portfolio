FROM python:3.10

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV CONFIG_FILE_PATH=""
COPY ./app /code/app

EXPOSE 80

CMD ["uvicorn", "app.server:app", "--port", "80", "--host", "0.0.0.0"]