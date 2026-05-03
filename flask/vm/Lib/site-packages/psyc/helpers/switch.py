import click
import json
import boto3
import sys
from .list import get_config_names

def switch_config(git_json, local_json):
    client = boto3.client("ssm")
    configs = list(get_config_names(git_json))
    previous_config = "NONE"
    if local_json != None:
        previous_config = local_json["config"]
    else:
        local_json = dict()

    click.echo(click.style("The following configs are available:", fg="green"))
    for i, name in enumerate(configs):
        if previous_config == name.split("/")[-1]:
            click.echo(f"\t {i+1}. {name} *")
        else:
            click.echo(f"\t {i+1}. {name}")

    # is there a way to truncate and show only some choices at a time? maybe in a while loop w a break?
    chosen_config = click.prompt(
        "Which number would you like to switch your local config to?",
        type=click.Choice([str(i + 1) for i in range(len(configs) + 1)]),
        show_default=False,
        show_choices=False,
        default = len(configs) + 1
    )

    # TODO: create a .state file if one doesn't exist when the config is switched

    chosen_config = int(chosen_config) - 1

    if chosen_config == len(configs):
        click.echo(click.style(f"CONFIG SWITCH CANCELLED", fg="yellow"))
        return

    local_json["config"] = configs[chosen_config].split("/")[-1]

    with open(".psyc.state", "w") as f:
        json.dump(local_json, f)

    click.echo(
        click.style(
            f"CHANGING CONFIG FROM {previous_config} TO {local_json['config']}",
            fg="red",
        )
    )
    param_name = f"{git_json['namespace']}/config/{local_json['config']}"

    try:
        print(
            client.get_parameter( Name=param_name, WithDecryption=True)['Parameter']['Value']
        )
    except:
        print(f"Exception: {sys.exc_info[0]} occurred. Parameter may not be found. Exiting program.")
        exit()
