import click
import json
import boto3
import sys
from .list import get_config_names

def delete_config(git_json, local_json):
    client = boto3.client("ssm")
    configs = list(get_config_names(git_json))
    if len(configs) == 0:
        click.echo(click.style("There are no configs available to delete for this project.", fg="red"))
        exit()
    click.echo(click.style("The following configs are available:", fg="green"))
    for i, name in enumerate(configs):
        if local_json and name.split("/")[-1] == local_json["config"]:
            click.echo(f"\t {i+1}. {name} *")
        else:
            click.echo(f"\t {i+1}. {name}")

    chosen_config = click.prompt(
        "Which config would you like to delete?",
        type=click.Choice([str(i + 1) for i in range(len(configs) + 1)]),
        show_default=False,
        show_choices=False,
        default=len(configs) + 1
    )
    chosen_config = int(chosen_config) - 1
    if chosen_config == len(configs):
        click.echo(click.style(f"CONFIG DELETE CANCELLED", fg="yellow"))
        return

    click.echo(click.style("The contents of this config are:", fg="green"))
    print(client.get_parameter(Name=configs[chosen_config], WithDecryption=True)['Parameter']['Value'])

    if not click.confirm('Are you sure you want to delete?'):
        click.echo(click.style(f'NOT DELETING {configs[chosen_config]}!', fg='yellow'))
        exit()
    try:
        response = client.delete_parameter(
            Name=configs[chosen_config]
        )
        click.echo(click.style(f"{configs[chosen_config]} successfully deleted!", fg="green"))
    except:
        print(f"Exception: {sys.exc_info[0]} occurred. Exiting program.")
        exit()
