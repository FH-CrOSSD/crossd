FROM python:3.13-alpine as build

WORKDIR /home/collector-drone
# RUN wget https://github.com/FH-CrOSSD/metrics/archive/refs/heads/main.zip -O - | unzip -
ARG VERSION=2.5.1
RUN wget https://github.com/FH-CrOSSD/metrics/archive/refs/tags/v${VERSION}.zip -O - \
    | unzip - && mv metrics-${VERSION} metrics
# install PDM
RUN pip install -U pip setuptools wheel --no-cache-dir
RUN pip install pdm --no-cache-dir
#RUN apk add build-base libffi-dev

WORKDIR /home/collector-drone/metrics
# WORKDIR /home/collector-drone/metrics-2
#RUN pdm config python.use_venv False
RUN mkdir __pypackages__ && pdm sync --prod --no-editable

FROM python:3.13-alpine 
#RUN apk add g++ libffi-dev
RUN pip install pdm --no-cache-dir
ENV PYTHONPATH=/project/pkgs
COPY --from=build /home/collector-drone/metrics/__pypackages__/3.13/lib /project/pkgs

# retrieve executables
COPY --from=build /home/collector-drone/metrics/__pypackages__/3.13/bin/* /bin/
WORKDIR /home/collector-drone
COPY . .
#RUN pdm config python.use_venv False
RUN pdm install
RUN pdm cache clear
RUN apk add git --no-cache

USER 1337:1337
ENTRYPOINT [ "pdm", "run", "worker"]
