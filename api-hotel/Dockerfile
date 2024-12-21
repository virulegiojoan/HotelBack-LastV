FROM python

WORKDIR /index

COPY /src .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "index:app" ]