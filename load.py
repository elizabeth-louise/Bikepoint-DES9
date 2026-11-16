import os
import json
import logging
import boto3 #library to connect with AWS
from dotenv import load_dotenv

# ----- Retrieving keys -----
load_dotenv() #access to .env file

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY') #directs to the env file and accessing the different variables
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# ----- Data file location -----
test_file = '2026-11-11 15-30-27.json'
file_location = 'data/2026-11-11 15-30-27.json'

# ----- Connecting to S3 -----
s3_client = boto3.client(
    's3', #what service we are trytrying to connect to
    aws_access_key_id = AWS_ACCESS_KEY, #this is case sensitive so don't mix the variables with what it is calling
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY #make sure lowercase to name the parameter 
)

# ----- Uploading file to bucket -----
s3_client.upload_file(file_location, AWS_BUCKET_NAME, test_file) #file location, the output location in S3, name of the file in the bucket

