This document provides a brief overview of ``PassPhraseScrambler``.

Basic Usage
===========

Overview
--------

PassPhraseScrambler provides both a command-line utility and a Python library for 
scrambling multiword passphrases such that they cannot be used without additional
information by an unwanted third party.

This section provides details of the command-line utility.

Installation
============

PassPhraseScrambler can be installed with ``pip``:

.. code-block:: console

    $ git clone git@github.com:tomjanus/passphrase-scrambler.git
    $ cd passphrase-scrambler
    $ pip install .

``PassPhraseScrambler`` usage may then be displayed with:

``pywrparser`` usage may then be displayed with:

.. code-block:: console

    $ passphrase --help

    Usage: passphrase [OPTIONS] COMMAND [ARGS]...

    --------------------- PASSPHRASE SCRAMBLER -----------------------

    You are using the Command Line Interface for word scrambler for encoding
    passphrases for encryption purposes.

    Limitations

        - requires words without spaces and alphanumeric symbols (i.e. pure
        letters only).

        - words cannot contain capital letters.

    Options:
    --help  Show this message and exit.

    Commands:
    scramble         Scrambles the original N-word passphrase.
    scramble-file    Scrambles the N-word passphrase in a file.
    unscramble       Un-scrambles the scrambled N-word passphrase.
    unscramble-file  Unscrambles the N-word passphrase in a file.


Passphrase scrambling
----------

Passphrase scrambler requires three pieces of information before it can `encode` the
original passphrase: the passphrase itself, the permutation sequence (order of words
in the scrambled passphrase), and the letter shift, i.e. by how many places in the letter
sequence each letter in every word is shifted. The information can be provided in the
command line.


or in the console

.. code-block:: console

    $ passphrase scramble --passphrase house,water,clock -perm 1,0,2 --verbose
    Scrambling ...
    Original passphrase: house, water, clock
    Permutation: 1, 0, 2
    Shift: 3
    Scrambled passphrase: zdwhu, krxvh, forfn

The ```passphrase``` argument defines the original passphrase as comma-delimited
sequence of words. If the sequence contains spaces, it needs to be wrapped around
double quotes, i.e. ```passphrase scramble --passphrase "house, water, clock" -perm 1,0,2 --verbose```. 
The same applies to the ```perm``` argument that defines the sequence of words in the scrambled
passphrase. The ```--verbose``` argument enables additional information to be output in the console.

The same information can be read from a text file, e.g.

.. code-block:: console

    passphrase scramble-file tests/passphrase_test.txt -v
    Scrambling passphrase: clock,  house,  flag,  kitesurfing,  window

    Permutation: 0, 3, 4, 2, 1

    Shift: 6

    Scrambled passphrase: iruiq, qozkyaxlotm, cotjuc, lrgm, nuayk


Passphrase unscrambling
----------

Passphrase unscrambling works in the same way as scrambling. The passsphrase for unscrambling
is provied in the ```--passphrase``` argument. The permutation pattern and the word shift
need to match the values provided during scrambling.

.. code-block:: console

    $ passphrase unscramble --passphrase "zdwhu, krxvh, forfn" -perm 1,0,2 --verbose
    Unscrambling ...
    Scrambled passphrase: zdwhu,  krxvh,  forfn
    Permutation: 1, 0, 2
    Shift: 3
    Original passphrase: house, water, clock

Using text input file:

.. code-block:: console

    $ passphrase unscramble-file tests/scrambled_passphrase_test.txt -v
    Unscrambling passphrase: iruiq,  qozkyaxlotm,  cotjuc,  lrgm,  nuayk

    Permutation: 0, 3, 4, 2, 1
    Shift: 6
    Unscrambled passphrase: clock, flag, house, window, kitesurfing

