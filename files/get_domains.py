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
    Get hostheader conditions from listeners for region.
    :param region:
    :return:
    """
    listeners = dict()

    types = json.loads(TYPES)
    elb_client = aws.get_elb_client(region)
    albs  = aws.get_load_balancers(elb_client, TAG, types)
    for alb in albs:
        listeners[alb] = aws.get_listener(elb_client, alb)

    logging.info(json.dump(listeners, indent=4))
    
