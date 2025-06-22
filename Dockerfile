FROM python:3.12-slim
WORKDIR /main
USER root
COPY . .

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 1008
CMD [ "python", "main.py" ]