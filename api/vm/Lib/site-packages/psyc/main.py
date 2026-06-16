import click
import json
from os.path import exists

from .helpers.list import get_config_names
from .helpers.switch import switch_config
from .helpers.new import create_config
from .helpers.edit import edit_config
from .helpers.delete import delete_config

@click.command()
@click.option('-l', '--list', is_flag=True, help = "List all available configs for the current project")
@click.option('-s', '--switch', is_flag=True, help = "Switch the local config to an existing config")
@click.option('-n', '--new', is_flag=True, help = "Create new, empty configuration entry in Parameter Store")
@click.option('-e', '--edit', is_flag=True, help = "Open config in editor and update in Parameter Store")
@click.option('-d', '--delete', is_flag=True, help = "Delete an existing config entry")
def main(list, switch, new, edit, delete):
    f1 = open('.psyc')
    git_json = json.load(f1)

    local_json = None
    if exists('.psyc.state'):
        f2 = open('.psyc.state')
        local_json = json.load(f2)

    click.echo(click.style(f'Working on project: {git_json["namespace"]}', fg='magenta'))

    if list:
        configs = get_config_names(git_json)
        if len(configs) == 0:
            click.echo(click.style('There are no configs available for this project.', fg="yellow"))

        click.echo(click.style('The available configs for this project are:', fg="green"))
        for _, name in enumerate(configs):
            if local_json and local_json["config"] == name.split('/')[-1]:
                click.echo(f"\t {name} *")
            else:
                click.echo(f"\t {name}")

    elif switch:
        switch_config(git_json, local_json)

    elif delete:
        delete_config(git_json, local_json)

    elif new:
        create_config(git_json)

    elif edit:
        if local_json == None:
            click.echo(click.style('A .psyc.state file does not exist in this directory. Please --init for this project, create a new config, or switch to an existing config', fg="red"))
            return
        edit_config(git_json, local_json)
