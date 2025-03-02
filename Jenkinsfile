pipeline {
    agent any

    parameters {
        string(name: 'EXECUTOR_ADDRESS', defaultValue: 'http://localhost:4444/wd/hub', description: 'Selenoid executor address')
        string(name: 'APPLICATION_URL', defaultValue: 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login', description: 'Application URL')
        string(name: 'BROWSER', defaultValue: 'chrome', description: 'Browser to use')
        string(name: 'THREADS', defaultValue: '1', description: 'Number of threads')
        string(name: 'BROWSER_VERSION', defaultValue: 'latest', description: 'Browser version')
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/rustemsam/otus_graduation'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Installing dependencies..."
                    pip install -r requirements.txt --break-system-packages
                    pip install --no-cache-dir pydantic-core --platform manylinux2014_x86_64 -t . --only-binary=:all: --break-system-packages
                '''
            }
        }
        stage('Run Tests') {
            parallel {
                stage('Frontend Tests') {
                    steps {
                        sh """
                            echo "Running frontend tests..."
                            python3 -m pytest --junit-xml=reports/frontend-junit.xml \
                            --alluredir=allure-results/frontend \
                            src/tests/frontend/pages/orm/test_recruitment.py \
                            src/tests/frontend/pages/orm/test_pim.py \
                            src/tests/frontend/pages/test_login.py
                        """
                    }
                }
                stage('Backend Tests') {
                    steps {
                        sh """
                            echo "Running backend tests..."
                            python3 -m pytest --junit-xml=reports/backend-junit.xml \
                                              --alluredir=allure-results/backend \
                                              src/tests/backend
                        """
                    }
                }
            }
        }
        stage('Generate Allure Reports') {
            steps {
                allure includeProperties: false, jdk: '', results: [
                    [path: 'allure-results/frontend'],
                    [path: 'allure-results/backend']
                ]
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*.xml', fingerprint: true
            junit 'reports/**/*.xml'
        }
        failure {
            echo "One or more tests failed! Check logs for details."
        }
    }
}