pipeline {
    agent any
    stages {
        stage('Deploy to AWS') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding', 
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                    credentialsId: 'cli_aws_keys', 
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    sh '''
                        echo "Hello"
                        // aws cloudformation deploy \
                        //     --template-file /path/to/template.yaml \
                        //     --stack-name my-stack \
                        //     --region eu-west-1 \
                        //     --parameter-overrides ParameterKey1=Value1 ParameterKey2=Value2
                        
                        // aws configure set region eu-west-1
                        // aws lambda invoke \
                        //     --function-name my-function \
                        //     response.json
                    '''
                }
            }
        }
    }
}