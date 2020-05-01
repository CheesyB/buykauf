FROM python:3.7
COPY . /buykauf
WORKDIR /buykauf
RUN pip install -r requirements.txt

CMD ["python", "baykauf/buy_kauf.py"]