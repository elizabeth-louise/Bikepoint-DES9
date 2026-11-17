import logging.config
import os
import json
import time
import logging
import requests

logger = logging.getLogger(__name__) #particular line of logging that attributes the logs that occur in this function to its own section in the logs - it will add the filename/function to the name of the log so it is distinguishable

def extract_to_json(url: str, data_dir: str,timestamp: str,  max_attempts: int,delay: int ): #defining the function, Args is the description of the function and each variable
    """Function to extract JSON files from a URL and save to a destination. 

    Args:
        url (str): URL to pull data from
        data_dir (str): filepath to save data to
        timestamp (str): timstamp to append to tfile name
        max_attempts (int): number of times to retry calls
        delay (int): how long to wait between call
    """
    # make directory if doesn't exist
    os.makedirs(data_dir, exist_ok= True)
    # build out the file name
    filename = f'{data_dir}/{timestamp}.json'

    attempt = 1

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
                
                return True # outcome of function is True/False - condition for next task would be that this task was successful - flag that data was saved successfully
            
            except Exception as e: #anything that goes wrong will store temporarily in e variable
                print(f'An error occurred when saving the JSON: {e}')
                logger.error(f'An error occurred when saving the JSON: {e}')
                
            break

        elif 300<= status_code <500:
            print(f'API call failed, status code {status_code} ☹️')
            logger.error(f'API call failed, status code {status_code} ☹️')
            break

        else:
            if attempt==max_attempts: 
                print(f'Max number of attempts reached. Status code {status_code}. Investigate further 🔍')
                logger.warning(f'Max number of attempts reached. Status code {status_code}. Investigate further 🔍')
            else:
                print(f'Attempt {attempt} failed, status code {status_code}. Trying again 😅')
                logger.error(f'Attempt {attempt} failed, status code {status_code}. Trying again 😅')

            attempt+=1 #increase the attempt variable
            time.sleep(delay) #wait 30s before retrying
    # return statement
    return False #if all retry events were unsuccessful then return False statement - don't want to do any other actions off the back of this function if unsuccessful - to stop any downstream functions being run so don't waste compute