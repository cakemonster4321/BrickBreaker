FROM python:3.13
WORKDIR /app
RUN ls -R /app
COPY . .
RUN pip3 install -r requirements.txt
CMD [ "python3","main.py"]
