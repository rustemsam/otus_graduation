pipeline {
    agent none

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
        stage('Checkout Code') {
            agent any
            steps {
                deleteDir()
                git branch: 'main', url: 'https://github.com/rustemsam/otus_graduation'
            }
        }

        stage('Install Dependencies') {
            agent any
            steps {
                sh '''
                    echo "Installing dependencies..."
                    pip install -r requirements.txt --break-system-packages
                    pip install --no-cache-dir pydantic-core --platform manylinux2014_x86_64 -t . --only-binary=:all: --break-system-packages
                '''
            }
        }

        stage('Run Tests in Parallel') {
            parallel {
                stage('Frontend Tests') {
                    agent { label 'frontend' }
                    steps {
                        script {
                            sh """
                            echo "Starting frontend tests with the following parameters:"
                            echo "Selenoid URL: ${params.SELENOID_URL}"
                            echo "Application URL: ${params.APPLICATION_URL}"
                            echo "Browser: ${params.BROWSER}"
                            echo "Browser Version: ${params.BROWSER_VERSION}"
                            echo "Threads: ${params.THREADS}"

                            python3 -m pytest --browser=${params.BROWSER} \\
                                              --remote \\
                                              --vnc \\
                                              --selenium_url=${params.SELENOID_URL} \\
                                              --alluredir=allure-results/frontend \\
                                              src/tests/frontend/pages/
                            """
                        }
                    }
                }

                stage('Backend Tests') {
                    agent { label 'backend' }
                    steps {
                        timeout(time: 5, unit: 'MINUTES') {
                            sh """
                                echo "Running backend tests..."
                                python3 -m pytest --junit-xml=reports/backend-junit.xml \\
                                                  --alluredir=allure-results/backend \\
                                                  src/tests/backend
                            """
                        }
                    }
                }
            }
        }

        stage('Generate Allure Reports') {
            agent any
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
