import click
import boto3
import sys

def edit_config(git_json, local_json):
    param_name = f"{git_json['namespace']}/config/{local_json['config']}"
    click.echo(click.style(f"Editing config: {param_name}", fg="yellow"))

    client = boto3.client("ssm")
    try:
        response = client.get_parameter(
                Name=param_name,
                WithDecryption=True
            )
    except:
        print(f"Exception: {sys.exc_info[0]} occurred. Exiting program.")
        exit()
        
    stored_config = response['Parameter']['Value']

    edited_config = click.edit(stored_config)
    if edited_config == stored_config or edited_config == None:
        click.echo(click.style(f"NO CHANGES MADE!", fg="green"))
        exit()
    
    # update parameter
    try:
        client.put_parameter(
            Name=param_name,
            Value=edited_config,
            Type='String',
            Overwrite=True
        )
    except:
        print(f"Exception: {sys.exc_info[0]} occurred. Exiting program.")
        exit()
    click.echo(click.style(f"Successfully changed the content of {param_name} to:", fg="green"))
    print(edited_config)