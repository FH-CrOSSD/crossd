FROM python:3.11-alpine as build

WORKDIR /home/collector-drone
# ARG GH_TOKEN
# ENV GH_TOKEN=$GH_TOKEN
RUN --mount=type=secret,id=ghtoken,target=/run/secrets/ghtoken \
 wget --header "Authorization: Bearer $(cat /run/secrets/ghtoken)" https://github.com/FH-CrOSSD/metrics/archive/refs/heads/main.zip -O - | unzip -
# RUN unzip main.zip 

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

WORKDIR /home/collector-drone/metrics-main
RUN mkdir __pypackages__ && pdm sync --prod --no-editable
# RUN pdm add pdm

# COPY . .
# RUN pip3 install -r requirements.txt
# # WORKDIR /home/collector-drone/MDI_Thesis
# RUN pip3 install -e MDI_Thesis
FROM python:3.11-alpine 
RUN pip install pdm
ENV PYTHONPATH=/project/pkgs
COPY --from=build /home/collector-drone/metrics-main/__pypackages__/3.11/lib /project/pkgs

# retrieve executables
COPY --from=build /home/collector-drone/metrics-main/__pypackages__/3.11/bin/* /bin/
WORKDIR /home/collector-drone
COPY . .
RUN pdm install
# RUN pip3 install -r requirements.txt
# RUN apk add coreutils
USER 1337:1337
# ENTRYPOINT [ "python3", "mdi_thesis/base.py"]
ENTRYPOINT [ "pdm", "run", "worker"]
# ENTRYPOINT [ "tail", "-f", "/dev/null"]