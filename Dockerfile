FROM python:3.13.1

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-chache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
