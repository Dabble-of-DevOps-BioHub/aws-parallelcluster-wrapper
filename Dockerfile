FROM continuumio/miniconda3:latest

USER root

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN conda install -y -c conda-forge pip

RUN mkdir -p /requirements
COPY environment.yml /requirements
COPY ./requirements* /requirements/
# All imports needed for autodoc.
RUN conda env create -f /requirements/environment.yml
RUN bash -c "source activate notebook &&  pip install -r /requirements/requirements_dev.txt -r /requirements/requirements.txt"
RUN echo "source activate notebook" >> ~/.bashrc

WORKDIR /app
ENV PYTHONPATH /app/:${PYTHONPATH}

#CMD make livehtml
