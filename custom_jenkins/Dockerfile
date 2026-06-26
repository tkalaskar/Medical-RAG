# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install Docker CLI, Trivy, and AWS CLI for image builds/scans/deploys from Jenkins.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl gnupg lsb-release unzip \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL -o /etc/apt/keyrings/docker.asc https://download.docker.com/linux/debian/gpg \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && . /etc/os-release \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian ${VERSION_CODENAME} stable" > /etc/apt/sources.list.d/docker.list \
    && curl -fsSL -o /tmp/trivy.key https://aquasecurity.github.io/trivy-repo/deb/public.key \
    && gpg --dearmor -o /usr/share/keyrings/trivy.gpg /tmp/trivy.key \
    && echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" > /etc/apt/sources.list.d/trivy.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli trivy \
    && case "$(dpkg --print-architecture)" in \
        amd64) aws_arch="x86_64" ;; \
        arm64) aws_arch="aarch64" ;; \
        *) echo "Unsupported AWS CLI architecture: $(dpkg --print-architecture)" >&2; exit 1 ;; \
    esac \
    && curl -fsSL -o /tmp/awscliv2.zip "https://awscli.amazonaws.com/awscli-exe-linux-${aws_arch}.zip" \
    && unzip -q /tmp/awscliv2.zip -d /tmp \
    && /tmp/aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli \
    && rm -rf /tmp/aws /tmp/awscliv2.zip /tmp/trivy.key \
    && rm -rf /var/lib/apt/lists/*

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
