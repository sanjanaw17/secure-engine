pipeline {
    agent any

    environment {
        IMAGE_TAG = "${env.GIT_COMMIT.take(7)}"
    }

    stages {

        stage('Clean Reports') {
            steps {
                sh '''
                rm -rf reports
                '''
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Gitleaks Scan') {
            steps {
                sh '''
                mkdir -p reports

                docker run --rm \
                  -v "$WORKSPACE":/repo \
                  -v "$WORKSPACE/reports":/reports \
                  zricethezav/gitleaks:latest \
                  detect \
                  --no-git \
                  --source=/repo \
                  --exit-code 1 \
                  --verbose \
                  --report-format=json \
                  --report-path=/reports/gitleaks-report.json
                '''

                archiveArtifacts artifacts: 'reports/gitleaks-report.json', fingerprint: true
            }
        }

        stage('Semgrep Scan') {
            steps {
                sh '''
                mkdir -p reports

                docker run --rm \
                  -v "$WORKSPACE":/src \
                  -v "$WORKSPACE/reports":/reports \
                  semgrep/semgrep \
                  semgrep \
                  --config=auto \
                  --json \
                  --output=/reports/semgrep-report.json \
                  /src
                '''

                archiveArtifacts artifacts: 'reports/semgrep-report.json', fingerprint: true
            }
        }

        stage('Build Docker Images') {
            steps {
                sh "docker build -t student-feedback-backend:${IMAGE_TAG} ./backend"
                sh "docker build -t student-feedback-frontend:${IMAGE_TAG} ./frontend"
            }
        }

        stage('Trivy Scan') {
            steps {
                sh '''
                mkdir -p reports

                docker run --rm \
                  -v /var/run/docker.sock:/var/run/docker.sock \
                  -v "$WORKSPACE/reports":/reports \
                  aquasec/trivy image \
                  --format json \
                  --output /reports/trivy-report.json \
                  student-feedback-backend:${IMAGE_TAG}
                '''

                archiveArtifacts artifacts: 'reports/trivy-report.json', fingerprint: true
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
