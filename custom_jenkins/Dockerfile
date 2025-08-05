# Use the Jenkins LTS base image
FROM jenkins/jenkins:lts

USER root

# Install Docker inside Jenkins container
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

# Add jenkins to docker group
RUN groupadd -f docker && usermod -aG docker jenkins
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to jenkins user
USER jenkins
