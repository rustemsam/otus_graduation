pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }

    parameters {
        string(name: 'SELENOID_URL', defaultValue: 'http://selenoid:4444/wd/hub', description: 'Selenoid executor URL')
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
        // Swap stages so that frontend tests run first.
        stage('Run Frontend Tests') {
            steps {
                script {
                    def selenoidUrl = params.SELENOID_URL
                    def appUrl = params.APPLICATION_URL
                    def browser = params.BROWSER
                    def browserVersion = params.BROWSER_VERSION
                    def threads = params.THREADS

                    sh """
                    echo "Starting frontend tests with the following parameters:"
                    echo "Selenoid URL: ${selenoidUrl}"
                    echo "Application URL: ${appUrl}"
                    echo "Browser: ${browser}"
                    echo "Browser Version: ${browserVersion}"
                    echo "Threads: ${threads}"

                    python3 -m pytest --browser=${browser} \
                                        --alluredir=allure-results/frontend \
                                        src/tests/frontend/pages/test_pim.py
                    """
                }
            }
        }
        stage('Run Backend Tests') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    sh """
                        echo "Running backend tests..."
                        python3 -m pytest --junit-xml=reports/backend-junit.xml \
                                          --alluredir=allure-results/backend \
                                          src/tests/backend
                    """
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
        echo "Build failed! Check logs for errors."
    }
}
}