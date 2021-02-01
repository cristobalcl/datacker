# Datacker base image
FROM python:3.8-slim as base
MAINTAINER Cristóbal Carnero Liñán "ccarnerolinan@gmail.com"
RUN pip install pip --upgrade && \
      pip install --no-cache-dir papermill && \
      pip install --no-cache-dir ipykernel
RUN mkdir notebooks && mkdir output
ADD datacker_runner /datacker_runner
ENTRYPOINT ["python", "-m", "datacker_runner.run"]

# Test the image
FROM base
RUN pip install --no-cache-dir pytest && \
      pip install --no-cache-dir nbformat
RUN cd datacker_runner && \
      pytest
ADD tests/test.ipynb /notebooks/
ADD tests/tests.sh /
RUN /tests.sh

FROM base
