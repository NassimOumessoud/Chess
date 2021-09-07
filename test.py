# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 12:41:00 2021

@author: Nassim
"""

import click

@click.command()
@click.option("--menu", prompt="Welcome to this 1v1 chess game, would you like to start a game?",
              help="The main menu.")
def begin(menu):
    """Main menu to start a game of chess."""
    if menu.lower() == 'yes' or 'y':
        click.echo("Let's start!")

if __name__ == '__main__':
    begin()
    
    
#@click.command()
#@click.option("--count", default=1, help="Number of greetings.")
#@click.option("--name", prompt="Your name",
#              help="The person to greet.")
#def hello(count, name):
#    """Simple program that greets NAME for a total of COUNT times."""
#    for _ in range(count):
#        click.echo("Hello, %s!" % name)
#
#if __name__ == '__main__':
#    hello()