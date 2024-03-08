import json
import boto3
import os
import uuid

findings_table=os.get_env("FINDINGS_TABLE_NAME")
def get_scan_findings(aws_account,repository_name, image_digest):
    ecr_client = boto3.client('ecr')
    response=ecr_client.describe_image_scan_findings(
        registryId=aws_account,
         repositoryName=repository_name,
        imageId={
            'imageDigest': image_digest
    },

    maxResults=1000

    )
    return response
    # paginator = ecr_client.get_paginator('describe_image_scan_findings')
    # response_iterator = paginator.paginate(
    #     repositoryName=repository_name,
    #     imageId={
    #         'imageDigest': image_digest
    #     }
    # )
    # findings = []
    # for page in response_iterator:
    #     findings.extend(page)
    #     if 'imageScanFindings' in page:
    #         findings.extend(page['imageScanFindings']['findings'])
    #         return findings
        
def save_finding(item_data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(findings_table)
    response = table.put_item(Item=item_data)
    return response   

def handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))
    findings=get_scan_findings(event['detail']['repository-name'], event['detail']['image-digest'])
    if 'imageScanFindings' in findings:

        for finding in findings:
            finding_data={
                "id":uuid.uuid4(),
                "registryId":findings['registryId'],
                "repositoryName": findings['repositoryName'],
                "imageDigest":findings['imageId']['imageDigest'],
                "scanDate":findings['imageScanFindings']['imageScanCompletedAt'],
                "findingName":finding['name'],
                "findingDescription":finding['description'],
                "findingUri":finding['uri'],
                "findingSeverity":finding['severity'],
                "findingAttributes":finding['attributes']

            }
            save_finding(finding_data)


    return {}