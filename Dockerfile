FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install newrelic

ENV NEW_RELIC_APP_NAME="App_flask"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=5f5195353176b018fb45fdd966ba0388FFFFNRAL
ENV NEW_RELIC_LOG_LEVEL=info

COPY . .

EXPOSE 5000

CMD ["python3", "application.py"]

ENTRYPOINT [ "newrelic-admin", "run-program" ]
