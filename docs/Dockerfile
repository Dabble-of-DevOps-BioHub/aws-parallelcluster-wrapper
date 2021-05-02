FROM jupyter/minimal-notebook

USER root

RUN apt-get update -y; apt-get upgrade -y; apt-get install -y openssh-server

USER jovyan

RUN conda install -y -c conda-forge pip

COPY ./requirements* /requirements/
COPY ./environment.yml /requirements/
RUN conda install --quiet --yes  -c conda-forge \
    'terraform=0.14.*' \
    'jq' \
     && \
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

RUN bash -c "pip install -r /requirements/requirements_dev.txt -r /requirements/requirements.txt"

ENV PYTHONPATH /home/jovyan/app:$PYTHONPATH

#WORKDIR /home/jovyan

#CMD make livehtml
