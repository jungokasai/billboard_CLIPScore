FROM pytorch/pytorch:1.7.1-cuda11.0-cudnn8-devel
COPY --from=python:3.7 / /

WORKDIR /

COPY . /

RUN pip install git+https://github.com/openai/CLIP.git
RUN pip install git+https://github.com/jungokasai/pycocoevalcap.git
RUN pip install -r requirements.txt
RUN pip install numpy==1.20.3

CMD ["/bin/bash"]
