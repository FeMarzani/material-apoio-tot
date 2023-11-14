import boto3
import logging

from utils.write_env import *

# Instanciando um cliente do S3.
def instantiate_client(resource: str):

    """Instantiate a new S3 Client and return it.
    :return: S3 Client instance
    """

    resource = str(resource).lower()

    client = boto3.client(resource, endpoint_url=ENDPOINT_URL,
                                aws_access_key_id=KEY_ID,
                                aws_secret_access_key=ACCESS_KEY,
                                region_name=REGION)

    logging.info(f'Instantiated a local ${resource} client.')
    
    return client