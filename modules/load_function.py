import os
import json
import logging
import boto3 #library to connect with AWS

logger = logging.getLogger(__name__)

def load_to_s3(AWS_ACCESS_KEY: str, AWS_SECRET_ACCESS_KEY: str, AWS_BUCKET_NAME: str, data_dir: str):
    """Function to load JSON files to S3 bucket.

    Args:
        AWS_ACCESS_KEY (str): AWS access key, use load_dotenv() to retrieve from .env file
        AWS_SECRET_ACCESS_KEY (str): AWS secret access key, use load_dotenv() to retrieve from .env file
        AWS_BUCKET_NAME (str): AWS S3 bucket name, use load_dotenv() to retrieve from .env file
        data_dir (str): directory to upload data from
    """
    # ----- Creating file location from file name -----
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
            logger.info(f'File {file} successfully uploaded!')
            os.remove(to_upload) #once uploaded, delete the file from the local save

            return True
        
        except Exception as e: #if something goes wrong with the upload
            print(f'Something went wrong. Error: {e}')#
            logger.error(f'Something went wrong. Error: {e}')

            return False