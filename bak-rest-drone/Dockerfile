FROM python:3.10-alpine as build

RUN apk add build-base chromium chromium-chromedriver

WORKDIR /home/collector-drone
# ARG GH_TOKEN
# ENV GH_TOKEN=$GH_TOKEN
RUN --mount=type=secret,id=ghtoken,target=/run/secrets/ghtoken \
    wget --header "Authorization: Bearer $(cat /run/secrets/ghtoken)" https://github.com/tobiasdam/thesis_metrics/archive/refs/heads/main.zip -O - | unzip -
# RUN unzip main.zip 

WORKDIR /home/collector-drone/thesis_metrics-main

RUN pip3 install -r requirements.txt
# WORKDIR /home/collector-drone/thesis_metrics-main
RUN pip3 install -e .

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

RUN mkdir -p outputs/logs && chown -R 1337:1337 outputs

# WORKDIR /home/collector-drone/thesis_metrics-main
# RUN mkdir __pypackages__ && pdm sync --prod --no-editable
# RUN pdm add pdm

# COPY . .
# RUN pip3 install -r requirements.txt
# # WORKDIR /home/collector-drone/MDI_Thesis
# RUN pip3 install -e MDI_Thesis
# FROM python:3.11-alpine 
# RUN pip install pdm
# ENV PYTHONPATH=/project/pkgs
# COPY --from=build /home/collector-drone/metrics-main/__pypackages__/3.11/lib /project/pkgs

# # retrieve executables
# COPY --from=build /home/collector-drone/metrics-main/__pypackages__/3.11/bin/* /bin/
WORKDIR /home/collector-drone
COPY . .
RUN pdm add -e /home/collector-drone/thesis_metrics-main --dev
RUN pdm install --dev
RUN mkdir -p /.cache/selenium && chown -R 1337:1337 /.cache/selenium
# RUN pip3 install -r requirements.txt
# RUN apk add coreutils
USER 1337:1337 
# ENTRYPOINT [ "python3", "mdi_thesis/base.py"]
ENTRYPOINT [ "pdm", "run", "worker"]
# ENTRYPOINT [ "tail", "-f", "/dev/null"]
