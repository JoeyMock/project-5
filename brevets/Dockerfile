FROM python:3.8
LABEL maintainer="jmock1881@gmail.com"
RUN apt-get update -y
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-B"]
CMD ["flask_brevets.py"]
#CMD ["hello.py"]
