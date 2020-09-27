FROM python:3.8.6-alpine3.12

EXPOSE 5000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

CMD [ "python", "-u", "./main.py" ]
