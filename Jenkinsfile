pipeline {
    agent {
        node {
            label 'ilgss0854.corp.amdocs.com'
        }
    }
    stages {
        stage('Deploy to AWS') {
            steps { 
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
