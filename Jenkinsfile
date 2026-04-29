pipeline {
    agent any

    parameters {
    choice(name: 'ENV', choices: ['dev', 'prod'], description: 'Deployment environment')
    }

    environment {
        PROJECT_ID = "project-7aaa7a69-7aef-409d-94b"
        REGION = "asia-south1"
        REPO = "weather-repo"
        IMAGE = "asia-south1-docker.pkg.dev/${PROJECT_ID}/${REPO}/weather-app:${BUILD_NUMBER}"
        ENV_NAME = "${params.ENV}"
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
                dir("terraform/environments/${params.ENV}") {
                    sh '''
                    rm -rf .terraform terraform.tfstate*
                    terraform init -input=false -reconfigure
                    terraform plan -out=tfplan \
                    -var="image=$IMAGE" \
                    -var-file="terraform.tfvars"
                    terraform apply -auto-approve tfplan
                    '''
                }

            }
        }

        stage('Health Check') {
            steps {
                dir("terraform/environments/${params.ENV}") {
                    sh '''
                    URL=$(terraform output -raw service_url)

                    # Retry logic (important)
                    for i in {1..5}; do
                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" $URL)
                    if [ "$STATUS" = "200" ]; then
                        echo "Health check passed"
                        exit 0
                    fi
                    echo "Retry $i: status=$STATUS"
                    sleep 5
                    done

                    echo "Health check failed. Rolling back..."

                    PREV=$(gcloud run revisions list \
                    --service weather-app-${ENV_NAME} \
                    --region asia-south1 \
                    --format="value(metadata.name)" \
                    --limit=2 | sed -n '2p')

                    if [ -z "$PREV" ]; then
                    echo "No previous revision found. Skipping rollback."
                    exit 1
                    fi

                    gcloud run services update-traffic weather-app-${ENV_NAME} \
                    --to-revisions=$PREV=100 \
                    --region asia-south1

                    exit 1
                    '''
                }
            }
        }
    }
}