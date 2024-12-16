FROM python:3.13
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]