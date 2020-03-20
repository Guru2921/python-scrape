FROM python:3
MAINTAINER guru.softwaremaster@gmail.command

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY maildriver.py ./
COPY webscrapping.py ./
COPY .env ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get -y install cron

# Copy Cron file
COPY cronfile /etc/cron.d/cronfile

# Give excution rights on the cron jobs
RUN chmod 0644 /etc/cron.d/cronfile

# Run cron job
RUN crontab /etc/cron.d/cronfile

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
# CMD [ "python", "webscrapping.py" ]