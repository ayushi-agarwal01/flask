FROM python:3.8-slim-buster
WORKDIR /neww - fixed
COPY requirements.txt .
#COPY . .
RUN pip install -r requirements.txt
COPY migrations/ migrations/
COPY app.py .
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]
