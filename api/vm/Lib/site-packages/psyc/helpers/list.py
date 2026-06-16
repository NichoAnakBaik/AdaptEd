import json
import boto3

def get_config_names(git_json):
    client = boto3.client("ssm")
    prefix = f"{git_json['namespace']}/config"

    # ! may be {namespace}/{config_name}/config
    params = client.describe_parameters(
        ParameterFilters=[
            {
                "Key": "Name",
                "Option": "Contains",
                "Values": [prefix],
            }
        ]
    )["Parameters"]

    config_names = set([param["Name"] for param in params])

    # list of all configs
    return config_names