FROM python:3.12-slim
WORKDIR /main
USER root
EXPOSE 1008

RUN apt-get update && apt-get install -y ffmpeg
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "main.py" ]