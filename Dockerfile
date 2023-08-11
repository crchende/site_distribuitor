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
COPY tests tests
COPY migrations migrations
COPY activeaza_venv activeaza_venv
COPY config.py config.py
COPY dockerstart.sh dockerstart.sh
COPY quickrequirements.txt quickrequirements.txt
COPY README.md README.md
COPY ruleaza_aplicatia ruleaza_aplicatia
COPY site_distribuitor.py site_distribuitor.py



RUN python -m venv .venv
RUN .venv/bin/pip install -r quickrequirements.txt

#WORKDIR /home/site/

# runtime configuration
EXPOSE 5010
ENTRYPOINT ["./dockerstart.sh"]
#CMD flask run --host 0.0.0.0 -p 5010
