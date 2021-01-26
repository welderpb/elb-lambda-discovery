import aws
import logging
import os
import json

TAG     = os.getenv('SKIP_TAG')
REGIONS = os.getenv('REGIONS')
TYPES   = os.getenv('TYPES')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event=None, context=None):
    """
    Event handler for AWS Lambda.
    :param event:
    :param context:
    :return:
    """
    regions = json.loads(REGIONS)
    for region in regions:
        get_domains(region)

def get_domains(region):
    """
    Get host entries from listeners for region.
    :param region:
    :return:
    """
    
    types = json.loads(TYPES)
    albs  = aws.get_load_balancers(region, TAG, types)
    logging.info(albs)
    
