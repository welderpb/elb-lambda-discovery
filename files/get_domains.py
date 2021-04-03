import aws
import logging
import os
import json
import urllib3

TAG     = os.getenv('SKIP_TAG')
REGIONS = os.getenv('REGIONS')
TYPES   = os.getenv('TYPES')
API_URL = os.getenv('API_URL')
SOURCE  = os.getenv('SOURCE')
GATEID  = os.getenv('GATEID')

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
    http = urllib3.PoolManager()

    for region in regions:
        albs = get_elb_data(region)
        data = prepare_post_data(albs, region)
        req  = http.request('POST', API_URL, body=json.dumps(data), headers = {'Content-Type': 'application/json'})
        logging.info(req.status)

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
        elbs[index].update({'listeners': aws.get_listeners(elb_client, alb['arn'])})
        for k, listener in enumerate(elbs[index]['listeners']):
            listener.update({"hostheaders": aws.get_hostheaders(elb_client, listener['arn'])})
            elbs[index]['listeners'][k] = listener

    #logging.info(json.dumps(elbs, indent=4))
    return elbs

def keep_first(iterable, key=None):
    if key is None:
        key = lambda x: x

    seen = set()
    for elem in iterable:
        k = key(elem)
        if k in seen:
            continue

        yield elem
        seen.add(k)

def prepare_post_data(albs, region):
    data = dict()
    data = {'data': [], 'source': SOURCE+region}

    for alb in albs:
        for listener in alb['listeners']:
            for host in listener['hostheaders']:
                data['data'].append({'fqdn':host,
                                     'tags': {
                                               'port': str(listener['port']),
                                               'region': region,
                                               'gate': GATEID
                                            }
                                    })

    #remove dublcates by fqdn
    #data['data'] = list(keep_first(data['data'], lambda d: d['fqdn']))
    #logging.info(json.dumps(data, indent=4))
    return data
