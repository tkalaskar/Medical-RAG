# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install Docker CLI only and add Jenkins to the docker group
RUN apt-get update -y && \
    apt-get install -y ca-certificates curl gnupg lsb-release docker-cli && \
    rm -rf /var/lib/apt/lists/*

# Add Jenkins user to the Docker group (create if it doesn't exist)
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Switch back to the Jenkins user
USER jenkins

# When running on macOS, mount the host Docker socket instead of installing Docker engine inside the container
# Example:
# docker run -d \
#     -v /var/run/docker.sock:/var/run/docker.sock \
#     -p 8080:8080 \
#     --name jenkins-dind \
#     jenkins-dind