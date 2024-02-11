import boto3
import re
import requests
import json
import logging
import os

username = "" 
password = ""
api_key = ""
api_url = ""
userpoolid = "i"
identity_pool_id = ""
    
def get_token():

    try:
        url = api_url
        payload = '{"username": "'+username+'", "password": "'+password+'"}'
        headers = {
            'x-api-key': api_key,
            'Content-Type': "application/json",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        json_response = json.loads(response.text)
        if json_response.get("status") == "success":
            token = json_response.get("id_token")
            return token
    except Exception as exception:
            logging.error("Error in get_token(): %s" % exception)
            print("Error in get_token()", exception)


def get_identity_id(temporary_token):
    try:
        cognitoidentity = boto3.client("cognito-identity", region_name="us-east-1")
        response = cognitoidentity.get_id(
            IdentityPoolId=identity_pool_id,
            Logins={
                'cognito-idp.{region}.amazonaws.com/{userpoolid}'.format(region="us-east-1",
                                                                         userpoolid=userpoolid): temporary_token
            }
        )
    except Exception as exception:
        logging.error("Seems to be an issue with Identity ID generation! Regenerating it again.. : %s" % exception)
        # raise exception
        print("Seems to be an issue with Identity ID generation! Regenerating it again..", exception)
#        expiration_time = datetime.now()
        return None
    else:
        return response["IdentityId"]

def get_creds():
    temp_token = get_token()
    try:
        cognitoidentity = boto3.client("cognito-identity", region_name="us-east-1")
        resp1 = cognitoidentity.get_credentials_for_identity(
            IdentityId=get_identity_id(temp_token),
            Logins={
                'cognito-idp.{region}.amazonaws.com/{userpoolid}'.format(region="us-east-1",
                                                                         userpoolid=userpoolid): temp_token
            }
        )
    except Exception as exception:
        logging.error("Error in get_creds(): %s" % exception)
        # raise exception
        print("Error in get_creds()", exception)
        return None, None, None
    else:
        secret_key = resp1["Credentials"]["SecretKey"]
        access_id = resp1["Credentials"]["AccessKeyId"]
        session_token = resp1["Credentials"]["SessionToken"]
        result = "{\"aws_access_key_id\":\""+access_id+"\",\"aws_secret_access_key\":\""+secret_key+"\",\"aws_session_token\":\""+session_token+"\",\"aws_id_token\":\""+temp_token+"\"}"
        return access_id, secret_key, session_token
    
def list_s3_object(access_id, secret_key, session_token, bucket_name):
    s3 = boto3.client('s3',
                      aws_access_key_id=access_id,
                      aws_secret_access_key=secret_key,
                      aws_session_token=session_token
                      )
    response = s3.list_objects(
        Bucket=bucket_name
    )
    file_name = [bucket["Key"] for bucket in response["Contents"] if bucket["Key"].endswith(".txt")]
    print(file_name)
    return file_name

def process_s3_file(file_names, access_id, secret_key, session_token, bucket_name):
    new_data = []
    for file_name in file_names:
        updated_file_name = file_name.split("/")[-1]
        with open(updated_file_name, "r") as f:
            data = f.readlines()
        print("Data: ",data)
        
        for each_line in data:
            if each_line.rstrip("\n") == "0":
                new_data.append(" ")
            else:
                if re.sub(r"\d+", "", each_line.strip("\n")):
                    new_data.append(each_line.rstrip("\n"))
        print(new_data)
        write_to_s3(new_data, file_name, access_id, secret_key, session_token, bucket_name)
        new_data.clear()

def write_to_s3(new_data, file_name_with_path, access_id, secret_key, session_token, bucket_name):
    s3 = boto3.client('s3',
                      aws_access_key_id=access_id,
                      aws_secret_access_key=secret_key,
                      aws_session_token=session_token
                      )
    with open("test1.txt", "w") as f1:
        f1.writelines(line + '\n' for line in new_data)
        print("File written successfully")
    
    s3.upload_file("test1.txt", bucket_name, file_name_with_path)
    print("File uploaded successfully to s3 bucket {}".format(bucket_name))
    os.remove("test1.txt")

def lambda_handler():
    access_id, secret_key, session_token = get_creds()
    bucket_name = 'atomiq-codepipeline-artifacts-dev-eu-central-1'
    
    # Get the file name from s3
    file_name = list_s3_object(access_id, secret_key, session_token, bucket_name)
    print("S3 file dev account:- ", json.dumps(file_name, indent=4, sort_keys=True))
    
    # Process the file and push it to s3
    process_s3_file(file_name,access_id, secret_key, session_token, bucket_name)
    
if __name__ == "__main__":
    lambda_handler()
    
