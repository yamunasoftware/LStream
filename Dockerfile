FROM python:3.12-slim
WORKDIR /main
USER root
COPY . .

RUN pip install --no-cache-dir flask waitress requests
EXPOSE 1008
CMD [ "python", "main.py" ]