FROM python:3.10-slim

ARG RUN_ID
ENV RUN_ID=${RUN_ID}
WORKDIR /app

RUN echo "Downloading model for Run ID: ${RUN_ID}" > /app/model_download.log

CMD ["sh", "-c", "echo Container started for Run ID: ${RUN_ID}; cat /app/model_download.log"]