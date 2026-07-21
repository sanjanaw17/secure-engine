pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
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
