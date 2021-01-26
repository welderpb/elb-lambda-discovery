import boto3
import logging

def get_elb_client(region='us-east-1'):
    elb_client = boto3.client('elbv2', region)
    return elb_client

def get_load_balancers(elb_client, skip_tag, types):
    """
    Returns loadbalncer arns for given region.
    :param region:
    :param skip_tag:
    :param types:
    :return: list
    """
    elb_client = boto3.client('elbv2', region)
    elb_response = elb_client.describe_load_balancers()

    elb_arns = [] # List to hold the elastic load balancers ARNs

    for i in elb_response.get('LoadBalancers'):
        if i['Type'] in types:
            elb_arns.append(i['LoadBalancerArn'])
   
    for elb in elb_arns:
        tags = elb_client.describe_tags(ResourceArns=[elb])
        for tag in tags.get('TagDescriptions')[0]['Tags']:
            if tag['Key'] == skip_tag:
                elb_arns.remove(elb)

    return elb_arns

def get_listener(elb_client, alb_arn):
    """
    Returns listeners arns for given loadbalancer.
    :param region:
    :param alb_arn:
    :return: list
    """
    elb_response = elb_client.describe_listeners(LoadBalancerArn=alb_arn)

    listeners = []

    for l in elb_response.get('Listeners'):
        if l['Protocol'] == 'HTTPS':
            listeners.append(l['ListenerArn'])

    return listeners


