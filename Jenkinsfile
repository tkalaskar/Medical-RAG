pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-southeast-2'
        ECR_REPO = 'my-repo'
        IMAGE_TAG = 'latest'
        IMAGE_PLATFORM = 'linux/amd64'
        ECS_CLUSTER = 'llmops-medical-service'
        SERVICE_NAME = 'llmops-medical-service'
    }

    stages {
        stage('Clone GitHub Repo') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'git_token', url: 'https://github.com/tkalaskar/Medical-RAG.git']])
                }
            }
        }

        stage('Build, Scan, and Push Docker Image to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
                        def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

                        sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
                        docker buildx version
                        docker buildx build --platform ${IMAGE_PLATFORM} -t ${env.ECR_REPO}:${IMAGE_TAG} --load .
                        trivy image --severity HIGH,CRITICAL --format json -o trivy-report.json ${env.ECR_REPO}:${IMAGE_TAG} || true
                        docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${imageFullTag}
                        docker push ${imageFullTag}
                        """

                        archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                    }
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {
                        echo "Triggering ECS deployment..."

                        sh """
                        aws ecs update-service \
                          --cluster ${ECS_CLUSTER} \
                          --service ${SERVICE_NAME} \
                          --force-new-deployment \
                          --region ${AWS_REGION}

                        aws ecs wait services-stable \
                          --cluster ${ECS_CLUSTER} \
                          --services ${SERVICE_NAME} \
                          --region ${AWS_REGION}
                        """
                    }
                }
            }
        }
    }
}
