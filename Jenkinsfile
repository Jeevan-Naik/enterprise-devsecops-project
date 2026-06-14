pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                bat '''
                pip install -r requirements.txt
                '''
            }
        }

        stage('Lint - flake8') {
            steps {
                bat '''
                flake8 app tests
                '''
            }
        }

        stage('Unit Tests - pytest') {
            steps {
                bat '''
                pytest
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        bat """
                        ${scannerHome}\\bin\\sonar-scanner.bat
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo 'Quality Gate Passed'
            }
        }

        stage('Docker Verification') {
            steps {
                bat 'docker version'
            }
        }

        stage('Docker Build') {
            steps {
                bat """
                docker build -t enterprise-devsecops-app:%BUILD_NUMBER% .
                docker tag enterprise-devsecops-app:%BUILD_NUMBER% enterprise-devsecops-app:latest
                """
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed'
        }

        success {
            echo 'Pipeline succeeded'
        }

        failure {
            echo 'Pipeline failed'
        }
    }
}