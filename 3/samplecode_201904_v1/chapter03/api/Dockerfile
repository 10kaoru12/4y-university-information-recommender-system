FROM python:3.6

EXPOSE 8000

WORKDIR /app
RUN apt update && apt install -y mecab libmecab-dev mecab-ipadic-utf8
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

CMD ["hug", "-f", "ml_api.py"]
