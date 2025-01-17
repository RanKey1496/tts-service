FROM debian AS model
RUN apt-get update && apt-get install -y sudo curl git
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get install git-lfs
RUN git lfs install
RUN git clone https://huggingface.co/coqui/XTTS-v2 /tmp/model
RUN rm -rf /tmp/model/.git

FROM python:3.9 as base
WORKDIR /app
COPY --from=model /tmp/model /app/models/XTTS-v2
RUN apt update
RUN apt-get install -y libsndfile1
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app

ENTRYPOINT ["python"]
CMD ["src/main.py"]