"""
Module that contains the command line application.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -m passphrase` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``passphrase.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``passphrase.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
from typing import Dict, Optional
import logging
import pathlib
import click
from pass_scrambler import PassPhrase, Permutation, PassPhraseScrambler

# Set up module logger
log = logging.getLogger(__name__)

FIGLET = True


@click.group()
def main() -> None:
    """--------------------- PASSPHRASE SCRAMBLER -----------------------

You are using the Command Line Interface for word scrambler for encoding
passphrases for encryption purposes. Limitations:
  - requires words without spaces and alphanumeric symbols (i.e. pure letters only)
  - words cannot contain capital letters
"""
click.echo(click.style("\nPASPHRASE SCRAMBLER", bg='blue', fg='black'))
click.echo(click.style("\n"))

default_passphrase = ['house', 'water', 'clock']
default_perm = ['0', '1', '2']
default_shift = 3
@click.command()
@click.option("-v", "--verbose", is_flag=True, 
              help="Generate more verbose outputs.")
@click.option('-p', '--passphrase', is_flag=False,  default=','.join(default_passphrase), show_default=True,
              type=click.STRING, help='Comma delimited list of words')
@click.option('-perm', '--permutation', is_flag=False,  default=','.join(default_perm), show_default=True,
              type=click.STRING, help='Comma delimited list of permutation indices (0-based)')
@click.option('-s', '--shift', is_flag=False, type=click.INT, default = default_shift, help='Letter shift (1-26)')   
def scramble(verbose: bool, passphrase: str, permutation: str, shift: int) -> None:
    """
    Scrambles the provided N-word passphrase.
    """
    word_list = [c.strip() for c in passphrase.split(',')]
    permutation_pattern = [int(c.strip()) for c in permutation.split(',')]
    if verbose:
        click.echo(click.style(f"Scrambling ..."))
        click.echo(click.style(f"Original passphrase: {word_list}"))
        click.echo(click.style(f"Permutation: {permutation_pattern}"))
        click.echo(click.style(f"Shift: {shift}"))
    mangler = PassPhraseScrambler(
        PassPhrase.from_string(passphrase), 
        Permutation.from_string(permutation), 
        shift)
    mangled_passphrase = mangler.encode()
    click.echo(click.style(
        f"Scrambled passphrase: {mangled_passphrase.words}"))
    

@click.command()
@click.option("-v", "--verbose", is_flag=True, 
              help="Generate more verbose outputs.")
@click.option('-p', '--passphrase', is_flag=False,  default=','.join(default_passphrase), show_default=True,
              type=click.STRING, help='Comma delimited list of words')
@click.option('-perm', '--permutation', is_flag=False,  default=','.join(default_perm), show_default=True,
              type=click.STRING, help='Comma delimited list of permutation indices (0-based)')
@click.option('-s', '--shift', is_flag=False, type=click.INT, default = default_shift, help='Letter shift (1-26)')   
def unscramble(verbose: bool, passphrase: str, permutation: str, shift: int) -> None:
    """
    Un-scrambles the provided N-word passphrase.
    """
    word_list = [c.strip() for c in passphrase.split(',')]
    permutation_pattern = [int(c.strip()) for c in permutation.split(',')]
    if verbose:
        click.echo(click.style(f"Unscrambling ..."))
        click.echo(click.style(f"Scrambled passphrase: {word_list}"))
        click.echo(click.style(f"Permutation: {permutation_pattern}"))
        click.echo(click.style(f"Shift: {shift}"))
    unmangler = PassPhraseScrambler(
        PassPhrase.from_string(passphrase), 
            permutation_pattern, 
            shift)
    unmangled_passphrase = unmangler.decode()
    click.echo(click.style(
        f"Original passphrase: {unmangled_passphrase.as_string()}"))


@click.command()
@click.argument('file', type=click.Path(exists=True))
def scramble_file(file: str) -> None:
    """
    Scrambles the provided N-word passphrase.
    """  
    mangler = PassPhraseScrambler.from_txt_file(file)
    click.echo(click.style(f"Scrambling passphrase: {mangler.passphrase.as_string()}"))
    mangled_passphrase = mangler.encode()
    click.echo(click.style(
        f"Scrambled passphrase: {mangled_passphrase.as_string()}"))


@click.command()
@click.argument('file', type=click.Path(exists=True))
def unscramble_file(file: str) -> None:
    """
    Unscrambles the provided N-word passphrase.
    """
    unmangler = PassPhraseScrambler.from_txt_file(file)
    click.echo(click.style(f"Unscrambling passphrase: {unmangler.passphrase.as_string()}"))
    unmangled_passphrase = unmangler.decode()
    click.echo(click.style(
        f"Unscrambled passphrase: {unmangled_passphrase.as_string()}"))


main.add_command(scramble)
main.add_command(unscramble)
main.add_command(scramble_file)
main.add_command(unscramble_file)
