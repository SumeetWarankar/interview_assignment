pipeline {
    agent {
        node {
            label 'test.com'
        }
    }
    stages {
        stage('Deploy to AWS') {
            steps { 
                script {
                    def awsCfnDeploy = load "deploy.groovy"
                    awsCfnDeploy.deploy_cft("lambda_cft.yaml", "s3-pull-push-lambda-function", "us-east-1", "24.04")
                }  
            }
        }
    }
}
