import aws
import logging
import os
import json

TAG     = os.getenv('SKIP_TAG')
REGIONS = os.getenv('REGIONS')
TYPES   = os.getenv('TYPES')
SOURCE  = 'AWS-QA'

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
        albs = get_elb_data(region)
        prepare_post_data(albs, region)

def get_elb_data(region):
    """
    Get hostheader conditions from listeners for region.
    :param region:
    :return:
    """
    elbs = list()

    types = json.loads(TYPES)
    elb_client = aws.get_elb_client(region)
    elbs  = aws.get_load_balancers(elb_client, TAG, types)
    for index, alb in enumerate(elbs):
        elbs[index].extend({'listeners': aws.get_listeners(elb_client, alb)})
        for k, listener in elbs[index]['listeners']:
            listener.update({"hostheaders": aws.get_hostheaders(elb_client, listener['arn'])})
            elbs[index]['listeners'][k] = listener

    logging.info(json.dumps(elbs, indent=4))
    return elbs
 
def prepare_post_data(albs, region):
    data = dict()
    data = {data: [], source: SOURCE}

    for alb in albs:
        for listener in alb['listeners']:
            for host in listener['hostheaders']:
                data['data'].append({'fqdn':host, 'namespace': region, port: listener['port']})

    logging.info(json.dumps(data, indent=4))
