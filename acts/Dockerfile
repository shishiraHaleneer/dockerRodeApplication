FROM centos:latest
ARG PORT=5000
WORKDIR /opt/acts

COPY . .

ENTRYPOINT ["/opt/acts/start.sh"]
# Add packages needed to build native dependencies
RUN curl https://bootstrap.pypa.io/get-pip.py | python && pip install flask
RUN chmod 777 start.sh

EXPOSE $PORT
CMD ["", $PORT]
