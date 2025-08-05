pipeline {
    agent any

    environment {
        PROJECT_ID = "alpine-proton-467708"
        SERVICE_NAME = "hotel-reservation-service"
        REGION = "us-central1"
        IMAGE = "gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gcp-creds')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/vedaantkadu/Mlops-Project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE} ."
            }
        }

        stage('Authenticate with GCP') {
            steps {
                sh 'gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS'
                sh "gcloud config set project $PROJECT_ID"
            }
        }

        stage('Push Docker Image to GCR') {
            steps {
                sh "gcloud auth configure-docker"
                sh "docker push ${IMAGE}"
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                sh """
                gcloud run deploy ${SERVICE_NAME} \
                    --image ${IMAGE} \
                    --platform managed \
                    --region ${REGION} \
                    --allow-unauthenticated
                """
            }
        }
    }
}
