pipeline {
    agent any

    environment {
        IMAGE_TAG = "${env.GIT_COMMIT.take(7)}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                sh "docker build -t student-feedback-backend:${IMAGE_TAG} ./backend"
                sh "docker build -t student-feedback-frontend:${IMAGE_TAG} ./frontend"
            }
        }

        stage('Start Pipeline') {
            steps {
                echo 'Pipeline Started Successfully!'
            }
        }

        stage('Finish') {
            steps {
                echo 'Pipeline Finished!'
            }
        }
    }
}
