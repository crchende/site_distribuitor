FROM python:3.8-alpine

ENV FLASK_APP site_distribuitor
#ENV FLASK_CONFIG = docker

#3.8 booster
#RUN useradd -rm -d /home/site -s /bin/bash -g root -G sudo -u 1001 site

#3.8 alpine
RUN adduser -D site

USER site

WORKDIR /home/site

COPY app app
COPY doc doc

RUN python -m venv .venv
RUN .venv/bin/pip install -r app/quickrequirements.txt

WORKDIR /home/site/app

# runtime configuration
EXPOSE 5010
ENTRYPOINT ["./dockerstart.sh"]
#CMD flask run --host 0.0.0.0 -p 5010
