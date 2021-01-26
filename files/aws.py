import boto3
import logging

def get_elb_client(region='us-east-1'):
    elb_client = boto3.client('elbv2', region)
    return elb_client

def get_load_balancers(elb_client, skip_tag, types):
    """
    Returns loadbalncer arns for given region.
    :param elb_client:
    :param skip_tag:
    :param types:
    :return: list
    """
    elb_response = elb_client.describe_load_balancers()

    elb_arns = [] # List to hold the elastic load balancers ARNs

    for l in elb_response.get('LoadBalancers'):
        if l['Type'] in types:
            elb_arns.append({'arn': l['LoadBalancerArn'],'scheme': l['Scheme']})
   
    for elb in elb_arns:
        tags = elb_client.describe_tags(ResourceArns=[elb['arn']])
        for tag in tags.get('TagDescriptions')[0]['Tags']:
            if tag['Key'] == skip_tag:
                elb_arns.remove(elb)

    return elb_arns

def get_listeners(elb_client, alb_arn):
    """
    Returns listeners arns for given loadbalancer.
    :param elb_client:
    :param alb_arn:
    :return: map
    """
    elb_response = elb_client.describe_listeners(LoadBalancerArn=alb_arn)

    listeners = list()

    for l in elb_response.get('Listeners'):
        if l['Protocol'] == 'HTTPS':
            listeners.append({'arn': l['ListenerArn'], 'port': l['Port']})

    return listeners

def get_hostheaders(elb_client, listener_arn):
    """
    Returns all hostheaders condition for given listener.
    :param elb_client:
    :param listener_arn:
    :return: list
    """
    hostheaders = []

    elb_response = elb_client.describe_rules(ListenerArn=listener_arn)
    for r in elb_response.get('Rules'):
        for cond in r['Conditions']:
            hostheader = cond.get('HostHeaderConfig')
            if hostheader:
                hostheaders.extend(hostheader['Values'])
    return hostheaders

