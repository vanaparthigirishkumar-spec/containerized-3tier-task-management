/**
 * Jenkins Declarative Pipeline — Containerized 3-Tier Application.
 *
 * Stages:
 *   1. Checkout source code
 *   2. Install Python dependencies
 *   3. Run backend tests (pytest)
 *   4. Validate Docker Compose configuration
 *   5. Build Docker images
 *
 * Jenkins requirements & permissions:
 *   - Jenkins agent must have Docker installed and the Jenkins user must be
 *     able to run Docker commands (e.g. jenkins user added to the 'docker'
 *     group, or Docker socket mounted / rootless Docker configured).
 *   - Python 3 and pip must be installed on the agent.
 *   - The Jenkins workspace needs write access to install Python packages
 *     and to create/remove test artefacts (e.g. test.db).
 *   - No cloud deployment is performed by this pipeline; it only builds
 *     images locally on the agent.
 *
 * Note: Do not claim this pipeline has run successfully unless it has
 * actually been executed in a configured Jenkins environment.
 */
pipeline {
    agent any

    environment {
        // Use sqlite for local/CI test runs unless a real test DB is configured.
        DATABASE_URL = 'sqlite:///./test.db'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout source code') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Install Python dependencies') {
            steps {
                echo 'Installing Python runtime and test dependencies...'
                sh '''
                pip install --upgrade pip
                pip install -r backend/requirements.txt -r tests/requirements.txt
                '''
            }
        }

        stage('Run backend tests') {
            steps {
                echo 'Running backend tests with pytest...'
                dir('backend') {
                    sh 'pytest tests -v'
                }
            }
        }

        stage('Validate Docker Compose configuration') {
            steps {
                echo 'Validating docker-compose.yml...'
                sh 'docker compose config --quiet'
            }
        }

        stage('Build Docker images') {
            steps {
                echo 'Building Docker images (frontend + backend)...'
                sh 'docker compose build'
            }
        }
    }

    post {
        always {
            echo 'Pipeline run complete.'
            // Clean up test artefacts created during the test stage.
            sh 'rm -f test.db .coverage' || true
        }
        failure {
            echo 'The pipeline failed. Review the stage logs above.'
        }
    }
}
