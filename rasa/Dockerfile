######################################################################
#  This Dockerfile is used build your Rasa image                     #
######################################################################

# RASA_IMAGE is passed from docker-compose.yml which is generated
# from ./botfront/docker-compose-template.yml and ./botfront/botfront.yml

FROM teploeodealko/rasa-for-botfront:2.3.3-e8-1.2.1

# Change back to root user to install dependencies
USER root

COPY . /custom/extensions/.

RUN pip install --no-cache-dir -r /custom/extensions/requirements.txt
RUN pip install -e /custom/extensions/.

# Switch back to non-root to run code
USER 1001