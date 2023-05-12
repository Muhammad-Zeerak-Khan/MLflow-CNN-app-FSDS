import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories, unzip_file
from src.utils.data_management  import validate_image
import random
import urllib.request as req



STAGE = "GET_DATA" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path):
    ## read config files
    config = read_yaml(config_path)
    URL = config["data"]["source_url"]
    local_dir = config["data"]["local_dir"]
    create_directories([local_dir])
    data_filename = config["data"]["data_filename"]
    data_filepath = os.path.join(local_dir, data_filename)
    
    
    if not os.path.isfile(data_filepath):
        logging.info("Downloading in progress...")
        filename, headers = req.urlretrieve(URL, data_filepath)
        logging.info(f"{data_filename} created with info \n {headers}")
    else:
        logging.info(f"filename : {data_filename} already exists")    

    #Unzip operation
    unzip_data_dir = os.path.join(config['data']['unzip_data_dir'])
    create_directories([unzip_data_dir])                                  
    unzip_file(source=data_filepath, dest = unzip_data_dir)

    #Validating data
    validate_image(config)




if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e