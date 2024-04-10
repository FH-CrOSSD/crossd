FROM python:3.11-alpine as build

WORKDIR /home/collector-drone
RUN wget https://github.com/FH-CrOSSD/metrics/archive/refs/heads/main.zip -O - | unzip -

# install PDM
RUN pip install -U pip setuptools wheel --no-cache-dir
RUN pip install pdm --no-cache-dir

WORKDIR /home/collector-drone/metrics-main
RUN mkdir __pypackages__ && pdm sync --prod --no-editable

FROM python:3.11-alpine 
RUN pip install pdm --no-cache-dir
ENV PYTHONPATH=/project/pkgs
COPY --from=build /home/collector-drone/metrics-main/__pypackages__/3.11/lib /project/pkgs

# retrieve executables
COPY --from=build /home/collector-drone/metrics-main/__pypackages__/3.11/bin/* /bin/
WORKDIR /home/collector-drone
COPY . .
RUN pdm install
RUN pdm cache clear

USER 1337:1337
ENTRYPOINT [ "pdm", "run", "worker"]