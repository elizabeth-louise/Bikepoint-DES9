import os
import json
import logging
import boto3 #library to connect with AWS
from dotenv import load_dotenv

# ----- Retrieving keys 🔑 -----
load_dotenv() #access to .env file

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY') #directs to the env file and accessing the different variables
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# ----- Data file location 📁 -----
data_dir = 'data'
# test_file = '2026-11-11 15-30-27.json'
file_location = os.listdir(data_dir) #lists everything in the data directory

# ----- Connecting to S3 🔗 -----
s3_client = boto3.client(
    's3', #what service we are trytrying to connect to
    aws_access_key_id = AWS_ACCESS_KEY, #this is case sensitive so don't mix the variables with what it is calling
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY #make sure lowercase to name the parameter 
)

# ----- Uploading file to bucket 🪣 -----
for file in file_location: #take each file in file_location (within the the data_dir)
    to_upload = f'{data_dir}/{file}' #creates the file path for each file in the data directory
    try:
        s3_client.upload_file(to_upload, AWS_BUCKET_NAME, file) #the file path for each file, the output location in S3, name of the file in the bucket
        print(f'File {file} successfully uploaded!')
        os.remove(to_upload) #once uploaded, delete the file from the local save
    except Exception as e: #if something goes wrong with the upload
        print(f'Something went wrong. Error: {e}')