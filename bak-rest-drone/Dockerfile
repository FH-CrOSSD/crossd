FROM python:3.10-alpine as build

# chromium stuff for selenium, tini as init for reaping zombies
RUN apk add --no-cache build-base chromium chromium-chromedriver tini

WORKDIR /home/collector-drone
# get thesis metrics library
RUN wget https://github.com/FH-CrOSSD/thesis_metrics/archive/refs/heads/main.zip -O - | unzip -

WORKDIR /home/collector-drone/thesis_metrics-main

# install thesis metrics library
RUN pip3 install -r requirements.txt --no-cache-dir 
RUN pip3 install -e . --no-cache-dir 

# install PDM
RUN pip install -U pip setuptools wheel --no-cache-dir 
RUN pip install pdm --no-cache-dir 

RUN mkdir -p outputs/logs && chown -R 1337:1337 outputs

WORKDIR /home/collector-drone
COPY . .
RUN pdm add -e /home/collector-drone/thesis_metrics-main --dev
RUN pdm install --dev
RUN pdm cache clear
RUN mkdir -p /.cache/selenium && chown -R 1337:1337 /.cache/selenium

USER 1337:1337 
ENTRYPOINT ["/sbin/tini", "--", "pdm", "run", "worker"]
