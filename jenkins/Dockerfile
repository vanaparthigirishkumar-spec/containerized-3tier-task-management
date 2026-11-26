# Custom Jenkins LTS image (JDK 21) with the Docker CLI installed.
#
# The Docker CLI is copied from the official docker:27-cli image so its
# version matches the Docker-in-Docker (docker:27-dind) build service.
# The host Docker socket is NOT mounted anywhere.

FROM docker:27-cli AS docker-cli

FROM jenkins/jenkins:lts-jdk21

# Plugins are installed at build time from plugins.txt using the official
# Jenkins plugin manager bundled in the image.
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

# Install Python tooling and the Docker CLI / Compose plugin.
# A virtualenv avoids PEP 668 "externally-managed-environment" errors and
# puts pip/pytest on PATH for the pipeline stages.
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/venv \
    && chown -R jenkins:jenkins /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

COPY --from=docker-cli /usr/local/bin/docker /usr/local/bin/docker
COPY --from=docker-cli /usr/local/libexec/docker/cli-plugins/docker-compose /usr/local/libexec/docker/cli-plugins/docker-compose
RUN chmod 755 /usr/local/bin/docker /usr/local/libexec/docker/cli-plugins/docker-compose

# Drop back to the unprivileged jenkins user.
USER jenkins

EXPOSE 8080 50000
