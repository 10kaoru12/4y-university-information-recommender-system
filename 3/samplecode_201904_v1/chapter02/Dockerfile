FROM jupyter/scipy-notebook:2c80cf3537ca

USER root
RUN apt update && apt install -y mecab libmecab-dev mecab-ipadic-utf8
RUN apt update && apt install -y jq

USER $NB_USER
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER