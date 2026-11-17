from datetime import datetime
from modules.extract_function import extract_to_json # from the folder and file path import the function created there
import logging
import os

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') #create datetime

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True) #os.makedirs makes the new directory, exist_ok allows it to be okay for the directory to already exist
log_filename = f'{log_dir}/{timestamp}.log' #logs have own file type

logging.basicConfig( #below is just how we want our logs to be configured, need to configure for it to know what we want to see
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s', #ascending time (puts the logs in order), levelname shows the severity of the message (i.e., error, warning),overall gives the layout of the log file
    level=logging.INFO #only thing below INFO is debug, debug gives lots of information
)

logger = logging.getLogger() #assigning logger to variable 
logger.info('Logger was successfully initialised.') #now when run, the log file will show this text - logger.info says we want to have it at an info level. #whereever have a print statement add a logger so it can record what happens, if its info then .info, if an error then .error

data_dir = 'data'

url = 'https://api.tfl.gov.uk/BikePoint/'

extract_result = extract_to_json(url,data_dir,timestamp,max_attempts=3,delay=30)

print(extract_result)