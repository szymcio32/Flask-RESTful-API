FROM python:3.6-alpine

WORKDIR /app

COPY requirements.txt /app
COPY app.py /app
COPY db.py /app

COPY common/ /app/common
COPY models/ /app/models
COPY resources/ /app/resources

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]