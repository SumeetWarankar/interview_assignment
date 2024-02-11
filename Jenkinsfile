pipeline {
    agent {
        node {
            label 'ilgss0854.corp.amdocs.com'
        }
    }
    stages {
        stage('Deploy to AWS') {
            steps { 
                script {
                    sh """
                        ls -larth
                        pwd
                    """
                    def awsCfnDeploy = load 'deploy.groovy'
                    awsCfnDeploy.deploy_cft('lambda_cft.yaml', 's3-pull-push-lambda-function', 'us-east-1')
                }  
            }
        }
    }
}
