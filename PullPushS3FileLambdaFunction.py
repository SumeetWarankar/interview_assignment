import boto3
import re
import json
import os

s3 = boto3.client('s3')

def list_s3_object(bucket_name):
    try:
        response = s3.list_objects(
            Bucket=bucket_name
        )
        file_name = [bucket["Key"] for bucket in response["Contents"] if bucket["Key"].endswith(".txt")]
        return file_name
    except Exception as e:
        print("Error: {}".format(e)) 

def process_s3_file(file_names, bucket_name):
    try:
        new_data = []
        for file_name_with_path in file_names:
            updated_file_name = file_name_with_path.split("/")[-1]
            
            # Download the file from S3 to the Lambda environment
            s3.download_file(bucket_name, file_name_with_path, '/tmp/' + updated_file_name)
        
            with open("/tmp/" + updated_file_name, "r") as f:
                data = f.readlines()
            print("Data: {}".format(data))
            
            for each_line in data:
                if each_line.rstrip("\n") == "0":
                    new_data.append(" ")
                else:
                    if re.sub(r"\d+", "", each_line.strip("\n")):
                        new_data.append(each_line.rstrip("\n"))
            print(new_data)
            write_to_s3(new_data, file_name_with_path, updated_file_name, bucket_name)
            new_data.clear()
    except Exception as e:
        print("Error: {}".format(e))

def write_to_s3(new_data, file_name_with_path, updated_file_name, bucket_name):
    try:
        with open("/tmp/" + updated_file_name, "w") as f1:
            f1.writelines(line + '\n' for line in new_data)
            print("File parsed successfully")
        
        s3.upload_file("/tmp/" + updated_file_name, bucket_name, file_name_with_path)
        print("File {} updated successfully to s3 bucket {}".format(updated_file_name, bucket_name))
    except Exception as e:
        print("Error: {}".format(e))

def lambda_handler(event, context):
    bucket_name = os.environ['S3_BUCKET_NAME']
    
    # Get the file name from s3
    file_name = list_s3_object(bucket_name)
    print("List of S3 files:- {}".format(json.dumps(file_name, indent=4, sort_keys=True)))
    
    # Process the file and push it to s3
    process_s3_file(file_name,bucket_name)
    