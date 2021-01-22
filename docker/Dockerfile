# Datacker base image
FROM python:3.8-slim as base
MAINTAINER Cristóbal Carnero Liñán "ccarnerolinan@gmail.com"
RUN pip install --no-cache-dir papermill
RUN pip install --no-cache-dir ipykernel
RUN mkdir notebooks && mkdir output
ADD run.py /
ENTRYPOINT ["python", "run.py"]

FROM base
RUN pip install --no-cache-dir nbformat
ADD test.ipynb /notebooks/
ADD tests.sh /
RUN /tests.sh

FROM base
