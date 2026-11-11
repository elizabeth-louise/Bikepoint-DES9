import logging.config
import os
import json
import time
import logging
from datetime import datetime #saves us having to write datetime.datetime every time
import requests #not a native package so have to pip install it, add the requirements .txt file with 'pip freeze >requirements.txt' in terminal

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') #create datetime

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True) #os.makedirs makes the new directory
log_filename = f'{log_dir}/{timestamp}.log' #logs have own file type

logging.basicConfig( #below is just how we want our logs to be configured, need to configure for it to know what we want to see
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s', #ascending time (puts the logs in order), levelname shows the severity of the message (i.e., error, warning),overall gives the layout of the log file
    level=logging.INFO #only thing below INFO is debug, debug gives lots of information
)

logger = logging.getLogger() #assining logger to variable 
logger.info('Logger was successfully initialised.') #now when run, the log file will show this text - logger.info says we want to have it at an info level. #whereever have a print statement add a logger so it can record what happens, if its info then .info, if an error then .error

data_dir = 'data' #the name of the directory, made it a variable so easily editable
os.makedirs(data_dir, exist_ok= True) #makes the folder
filename = f'{data_dir}/{timestamp}.json' #this creates the variable #allowed spaces in filenames, good to think about what characters not allowed i.e., ':'

url = 'https://api.tfl.gov.uk/BikePoint/' #API endpoint

attempt = 1
max_attempts = 3

while attempt <= max_attempts: #run the following until the max attempts is reached
    response = requests.get(url)
    status_code = response.status_code

    if 200<= status_code <300: #if status code between 200 and 300
        try: #if anything goes wrong within the try (here this is saving the file) then exit out and execute anything in the except #good practice to put in error handling
            data = response.json() #returns the repsonse we have from the API into JSON #create the file from filename and write into it (line 19), then dump the json data into the file (line 20)
            with open(filename,'w') as file: #'w' means write into the file
                json.dump(data, file) #aliasing the open(filename, 'w') as file so don't have to repeat it
            print(f'File {filename} saved successfully 🎉')
            logger.info(f'File {filename} saved successfully 🎉')
        except Exception as e: #anything that goes wrong will store temporarily in e variable
            print(f'An error occured when saving the JSON: {e}')
            logger.error(f'An error occured when saving the JSON: {e}')
            
        
        break

    elif 300<= status_code <500:
        print(f'API call falied, status code {status_code} ☹️')
        logger.error(f'API call falied, status code {status_code} ☹️')
        break

    else:
        if attempt==max_attempts: 
            print(f'Max number of attempts reached. Status code {status_code}. Investigate further 🔍')
            logger.warning(f'Max number of attempts reached. Status code {status_code}. Investigate further 🔍')
        else:
            print(f'Attempt {attempt} failed, status code {status_code}. Trying again 😅')
            logger.error(f'Attempt {attempt} failed, status code {status_code}. Trying again 😅')

        attempt+=1 #increase the attempt variable
        time.sleep(30) #wait 30s before retrying



        