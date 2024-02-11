def deploy_cft(String templatePath, String stackName, String region, String releaseVersion) {
    sh """
        aws cloudformation deploy \
            --template-file ${templatePath} \
            --stack-name ${stackName} \
            --capabilities CAPABILITY_IAM \
            --profile cliaws \
            --region ${region} \
            --parameter-overrides ReleaseVersion=${releaseVersion}
    """
}
return this
