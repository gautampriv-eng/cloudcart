pipeline {
    agent any

    triggers {
        // Poll SCM every 2 minutes for automated CI triggers on code push
        pollSCM('H/2 * * * *')
    }

    environment {
        APP_NAME = "todo-api"
        BUILD_TIMESTAMP = sh(script: 'date +%Y%m%d%H%M%S', returnStdout: true).trim()
        GIT_COMMIT_SHORT = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        VERSION_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT_SHORT}"
        DOCKER_IMAGE = "${APP_NAME}:${VERSION_TAG}"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '5'))
        timeout(time: 15, unit: 'MINUTES')
        timestamps()
        ansiColor('xterm')
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo "=========================================================="
                echo "Stage 1: Checking out source code from Git repository"
                echo "Commit SHA: ${env.GIT_COMMIT_SHORT}"
                echo "Build Number: ${env.BUILD_NUMBER}"
                echo "=========================================================="
                checkout scm
            }
        }

        stage('Code Quality & Lint') {
            steps {
                echo "=========================================================="
                echo "Stage 2: Code Quality and PEP8 Static Analysis"
                echo "=========================================================="
                sh '''
                    python3 -m pip install --upgrade pip flake8
                    flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics || true
                '''
            }
        }

        stage('Automated Unit Tests') {
            steps {
                echo "=========================================================="
                echo "Stage 3: CI Enhancement - Running Automated Unit Tests"
                echo "=========================================================="
                sh '''
                    python3 -m pip install -r requirements.txt
                    python3 -m pytest -v --junitxml=reports/test-results.xml tests/
                '''
            }
            post {
                always {
                    junit testResults: 'reports/test-results.xml', allowEmptyResults: true
                }
            }
        }

        stage('Package Build Artifact') {
            steps {
                echo "=========================================================="
                echo "Stage 4: Packaging Application Release Bundle"
                echo "=========================================================="
                sh '''
                    mkdir -p dist
                    tar -czf dist/${APP_NAME}-v${VERSION_TAG}.tar.gz app/ requirements.txt
                    echo "Successfully generated artifact: dist/${APP_NAME}-v${VERSION_TAG}.tar.gz"
                '''
            }
        }

        stage('Container Image Build & Versioning') {
            steps {
                echo "=========================================================="
                echo "Stage 5: CI Enhancement - Versioned Docker Image Build"
                echo "Tagging Docker Image with Commit SHA: ${DOCKER_IMAGE}"
                echo "=========================================================="
                sh '''
                    docker build -t ${DOCKER_IMAGE} -t ${APP_NAME}:latest .
                    echo "Docker image ${DOCKER_IMAGE} built and tagged."
                '''
            }
        }

        stage('Smoke & Health Test') {
            steps {
                echo "=========================================================="
                echo "Stage 6: Container Smoke Test and Health Verification"
                echo "=========================================================="
                sh '''
                    docker run -d --name ${APP_NAME}-smoke -p 5001:5000 ${DOCKER_IMAGE}
                    sleep 3
                    curl --fail --retry 3 http://localhost:5001/health || exit 1
                    docker rm -f ${APP_NAME}-smoke
                    echo "Smoke test passed successfully."
                '''
            }
        }
    }

    post {
        always {
            echo "=========================================================="
            echo "Archiving Build Artifacts and Test Results"
            echo "=========================================================="
            archiveArtifacts artifacts: 'dist/*.tar.gz, reports/*.xml', fingerprint: true, allowEmptyArchive: true
            cleanWs deleteDirs: true, notFailBuild: true
        }
        success {
            echo "[SUCCESS] Jenkins Pipeline execution completed successfully for Build #${env.BUILD_NUMBER}!"
        }
        failure {
            echo "[FAILURE] Pipeline build failed. Please inspect console logs."
        }
    }
}
