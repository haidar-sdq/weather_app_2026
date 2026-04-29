pipeline {
    agent any

    parameters {
    choice(name: 'ENV', choices: ['dev', 'prod'])
    }

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
                --config=cloudbuild.yaml \
                --substitutions=_IMAGE=$IMAGE
                '''
            }
        }

        stage('Approve Prod Deployment') {
            when {
                expression { params.ENV == 'prod' }
            }
            steps {
                input message: "Approve deployment to PROD?"
            }
        }

        stage('Terraform Deploy') {
            steps {
                dir("terraform/environments/${ENV}") {
                    sh '''
                    terraform init -input=false -reconfigure
                    terraform plan -out=tfplan -var="image=$IMAGE"
                    terraform apply -auto-approve tfplan
                    '''
                }

            }
        }

        stage('Health Check') {
            steps {
                dir("terraform/environments/${ENV}") {
                    sh '''
                    URL=$(terraform output -raw service_url)

                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" $URL/api/v1/weather/Delhi)

                    if [ "$STATUS" != "200" ]; then
                    echo "Health check failed. Rolling back..."

                    PREV=$(gcloud run revisions list \
                        --service weather-app-${ENV} \
                        --region asia-south1 \
                        --format="value(metadata.name)" \
                        --limit=2 | tail -n 1)

                    gcloud run services update-traffic weather-app-${ENV} \
                        --to-revisions=$PREV=100 \
                        --region asia-south1

                    exit 1
                    fi
                    '''
                }
            }
        }
    }
}