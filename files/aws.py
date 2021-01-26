import boto3
import logging

def get_load_balancers(region='us-east-1', skip_tag='', types=["application"]):
    """
    Returns instances data for given asg.
    :param region:
    :param skip_tag:
    :param types:
    :return: map
    """
    elb_client = boto3.client('elbv2', region)
    elb_response = elb_client.describe_load_balancers().get('LoadBalancers')

    elb_arns = [] # List to hold the elastic load balancers ARNs

    for i in elb_response.get('LoadBalancers'):
        if i.Type in types:
            elb_arns.append(i['LoadBalancerArn'])
   
    for elb in elb_arns:
        tags = elb_client.describe_tags(ResourceArns=[elb])
        for tag in tags.get('TagDescriptions')[0]['Tags']:
            if tag['Key'] == skip_tag:
                elb_arns.remove(elb)

    return elb_arns

