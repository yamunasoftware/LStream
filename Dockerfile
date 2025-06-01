FROM python:3.8-slim
WORKDIR /main
USER root

COPY main.py .
COPY index.html .

RUN pip install --no-cache-dir flask waitress
EXPOSE 1008
CMD [ "python", "main.py" ]