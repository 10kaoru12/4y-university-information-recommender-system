FROM python:3.6-alpine

WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8000

ENTRYPOINT ["hug"]
CMD ["-f", "app.py"]