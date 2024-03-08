import boto3
import json

def start_image_scan():
    ecr_client = boto3.client('ecr')

    # Create a paginator for listing repositories
    paginator = ecr_client.get_paginator('describe_repositories')
    response_iterator = paginator.paginate()

    # Iterate over the pages of repositories
    for page in response_iterator:
        repositories = page['repositories']
        
        # Start image scan for each repository
        for repository in repositories:
            repository_name = repository['repositoryName']
            paginator_images = ecr_client.get_paginator('list_images')
            response_iterator_images = paginator_images.paginate(repositoryName=repository_name)

            for images_page in response_iterator_images:
                images= images_page['imageIds']
                for image in images:
                    ecr_client.start_image_scan(repositoryName=repository_name,imageId=image)
                    print(f"Manual image scan started for {repository_name}:{image['imageDigest']}")
def handler(event, context):
    start_image_scan()

    return {}