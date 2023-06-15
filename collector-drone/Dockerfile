FROM python:3.11-alpine as build

WORKDIR /home/collector-drone
COPY . .
RUN pip3 install -r requirements.txt
# WORKDIR /home/collector-drone/MDI_Thesis
RUN pip3 install -e MDI_Thesis

USER 1337:1337
# ENTRYPOINT [ "python3", "mdi_thesis/base.py"]
ENTRYPOINT [ "python3", "test.py"]