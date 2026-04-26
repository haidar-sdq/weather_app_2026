pipeline {
    agent any

    environment {
        PROJECT_ID = "project-7aaa7a69-7aef-409d-94b"
        REGION = "asia-south1"
        REPO = "weather-repo"
        IMAGE = "asia-south1-docker.pkg.dev/${PROJECT_ID}/${REPO}/weather-app:${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Verify Tools') {
            steps {
                sh '''
                docker --version
                terraform --version
                gcloud --version
                '''
            }
        }

        stage('Build & Push Image') {
            steps {
                sh '''
                gcloud auth configure-docker asia-south1-docker.pkg.dev -q
                gcloud builds submit \
                --service-account=projects/project-7aaa7a69-7aef-409d-94b/serviceAccounts/cloud-build-sa-465881762218@project-7aaa7a69-7aef-409d-94b.iam.gserviceaccount.com \
                --tag $IMAGE
                '''
            }
        }

        stage('Terraform Deploy') {
            steps {
                dir('terraform') {
                    sh '''
                    terraform init
                    terraform apply -auto-approve \
                      -var="image=$IMAGE"
                    '''
                }
            }
        }
    }
}