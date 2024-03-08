FROM python:3.11

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "gensresponse"]