FROM python:3

WORKDIR /usr/src/app

ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV BOT_TOKEN "$VIRTUAL_ENV/bin:$BOT_TOKEN"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY .env .

CMD [ "python", "main.py" ]