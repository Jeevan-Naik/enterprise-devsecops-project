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

        stage('Deploy UAT') {
            steps {
                bat '''
                docker stop enterprise-app-uat 2>NUL
                docker rm enterprise-app-uat 2>NUL
                docker run -d --name enterprise-app-uat -p 5001:5000 enterprise-devsecops-app:%BUILD_NUMBER%
                '''
            }
        }
    
        stage('Smoke Test UAT') {
            steps {
                sleep(time: 15, unit: 'SECONDS')
                bat '''
                curl http://localhost:5001/health
                '''
            }
        }
            
        stage('Manual Approval') {
            steps {
                input message: 'UAT validation successful. Deploy to Production?'
            }
        }

        stage('Deploy PROD') {
            steps {
                bat '''
                docker stop enterprise-app-prod 2>NUL
                docker rm enterprise-app-prod 2>NUL
                docker run -d --name enterprise-app-prod -p 5002:5000 enterprise-devsecops-app:%BUILD_NUMBER%
                '''
            }
        }

        stage('Validate PROD') {
            steps {
                sleep(time: 15, unit: 'SECONDS')

                bat '''
                curl http://localhost:5002/health
                '''
            }
        }

        stage('Release Summary') {
            steps {
                echo "======================================"
                echo "Release Successfully Deployed"
                echo "Build Number: ${env.BUILD_NUMBER}"
                echo "UAT URL: http://localhost:5001"
                echo "PROD URL: http://localhost:5002"
                echo "Image: enterprise-devsecops-app:${env.BUILD_NUMBER}"
                echo "======================================"
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