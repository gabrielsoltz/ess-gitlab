FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt && apt-get update -y && apt-get install curl jq -y

COPY . /usr/src/app

CMD ["echo", "This is a 'Purpose-Built Container', It is not meant to be ran this way. Run this in a CI Pipeline."]
