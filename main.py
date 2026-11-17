from datetime import datetime
from modules.extract_function import extract_to_json # from the folder and file path import the function created there
from modules.load_function import load_to_s3
import logging
import os
from dotenv import load_dotenv

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') #create datetime

# ----- Setup logging 🪵-----
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True) #os.makedirs makes the new directory, exist_ok allows it to be okay for the directory to already exist
log_filename = f'{log_dir}/{timestamp}.log' #logs have own file type

logging.basicConfig( #below is just how we want our logs to be configured, need to configure for it to know what we want to see
    filename=log_filename,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', #name adds the extract_function within the log
    level=logging.INFO #only thing below INFO is debug, debug gives lots of information
)

logger = logging.getLogger() #assigning logger to variable 
logger.info('Logger was successfully initialised.') #now when run, the log file will show this text - logger.info says we want to have it at an info level. #whereever have a print statement add a logger so it can record what happens, if its info then .info, if an error then .error

# ----- Declare variables 💬-----
data_dir = 'data'

url = 'https://api.tfl.gov.uk/BikePoint/'

# ----- Using extract function -----
extract_result = extract_to_json(
    url,
    data_dir,
    timestamp,
    max_attempts=3,
    delay=30
)

print(extract_result)

# ----- Retrieving keys 🔑 -----
load_dotenv() #access to .env file

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY') #directs to the env file and accessing the different variables
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# ----- Using load function 🔃-----
load_result = load_to_s3(
    AWS_ACCESS_KEY,
    AWS_SECRET_ACCESS_KEY,
    AWS_BUCKET_NAME,
    data_dir
)

print(load_result)