import click
import boto3
import sys
from .list import get_config_names

def create_config(git_json):
    client = boto3.client('ssm')
    prefix = f"{git_json['namespace']}/config"

    # prompt user input
    click.echo(f'The new config will be created with the prefix: {click.style(f"{prefix}/...", fg="green")}\n')
    while True:
        new_config_name = click.prompt(
            "What would you like to name this config?",
            show_default=False,
            show_choices=False,
            default = ""
        )
        if new_config_name == "":
            click.echo(click.style("No name entered. Cancelling config creation.", fg="yellow"))
            return

    # check for an existing config with the input name
    existing_configs = get_config_names(git_json)
    new_config_path = f'{prefix}/{new_config_name}'
    if new_config_path in existing_configs:
        click.echo(
            f'A config named {click.style(new_config_path, fg="red")} already exists. Please use ' +
                f'{click.style(f"python3 main.py -s", fg="green")} to switch to this config or use a different name.'
            )
        exit()
    try:
        response = client.put_parameter(
            Name = new_config_path,
            Value = "{}",
            Type="SecureString"
        )
        click.echo(click.style(f"Successfully created config with name {new_config_path}", fg="green"))
    except:
        print(f"Exception: {sys.exc_info[0]} occurred. Exiting program.")
        exit()
