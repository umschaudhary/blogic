FROM python:3.8-slim
MAINTAINER umeshchaudhary@gmail.com

COPY . /blogic
WORKDIR /blogic

RUN pip install -r requirements/base.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
