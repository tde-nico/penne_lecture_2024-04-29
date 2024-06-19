FROM python:3.10

RUN apt update && \
	python3 -m pip install -U flask

WORKDIR /home/cc/
COPY ./ .
EXPOSE 1337

CMD [ "python3", "app.py"]