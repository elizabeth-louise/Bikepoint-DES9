import os
import json
import time
from datetime import datetime #saves us having to write datetime.datetime every time
import requests #not a native package so have to pip install it, add the requirements .txt file with 'pip freeze >requirements.txt' in terminal

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') #create datetime
data_dir = 'data' #the name of the directory, made it a variable so easily editable
os.makedirs(data_dir, exist_ok= True) #makes the folder
filename = f'{data_dir}/{timestamp}.json' #this creates the variable
#allowed spaces in filenames, good to think about what characters not allowed i.e., ':'

url = 'https://api.tfl.gov.uk/BikePoint/' #API endpoint

attempt = 1
max_attempts = 3

while attempt <= max_attempts: #run the following until the max attempts is reached
    response = requests.get(url)
    status_code = response.status_code

    if 200<= status_code <300: #if status code between 200 and 300
        data = response.json() #returns the repsonse we have from the API into JSON
        
        #create the file from filename and write into it (line 19), then dump the json data into the file (line 20)
        with open(filename,'w') as file: #'w' means write into the file
            json.dump(data, file) #aliasing the open(filename, 'w') as file so don't have to repeat it
        
        print(f'File {filename} saved successfully 🎉')
        
        break

    elif 300<= status_code <500:
        print(f'API call falied, status code {status_code} 👎☹️')
        break

    else:
        if attempt==max_attempts:
            print(f'Max number of attempts reached. Status code {status_code}. Investigate further 🔍')
        else:
            print(f'Attempt {attempt} failed, status code {status_code}. Trying again 😅')

        attempt+=1 #increase the attempt variable
        time.sleep(30)



        