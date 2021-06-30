import enum
import os.path
import random
from dataclasses import dataclass

import pytest
from ..app.main import retrieve_users, save_text_in_file, Mutant, Powers, MutantFamily, MutantStrength, fight_mutants


# Notice the name of the parameter which is the exact same name of the fixture that we defined before
def test_retrieve_users(db_connection):
    assert retrieve_users(db_connection) == "All users"


def test_write_text_to_file(tmpdir):
    file_name = "dummy_file.txt"
    file_path = os.path.join(tmpdir, file_name)
    text_to_write = "Hello World"
    save_text_in_file(text_to_write, file_path)
    with open(file_path, 'r') as fp:
        assert fp.readline() == text_to_write


def test_fight_mutants(get_mutant_generator):
    mutant_army = get_mutant_generator(100)
    last_survivor = fight_mutants(mutant_army)
    assert last_survivor.power.name in Powers.__members__
    assert last_survivor.family.name in MutantFamily.__members__
    assert last_survivor.strength.name in MutantStrength.__members__
