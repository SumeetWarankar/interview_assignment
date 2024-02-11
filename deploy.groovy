def deploy_cft(String templatePath, String stackName, String region) {
    sh """
        aws cloudformation deploy \
            --template-file ${templatePath} \
            --stack-name ${stackName} \
            --capabilities CAPABILITY_IAM \
            --profile cliaws
            --region ${region}
    """
}