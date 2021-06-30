import random

import pytest

from ..app.main import DummyDb, Powers, MutantStrength, MutantFamily, Mutant


@pytest.fixture
def db_connection():
    conn = DummyDb()
    conn.connect()
    return conn



# Solution for the exercise : DONT LOOK AT IT IF YOU DID NOT TRY BY YOUR OWN BEFORE !!!

@pytest.fixture
def get_mutant_generator():
    def mutant_generator(number_of_mutants):
        mutant_army = []
        for m in range(0, number_of_mutants):
            power = random.choice(list(Powers))
            strength = random.choice(list(MutantStrength))
            family = random.choice(list(MutantFamily))
            mutant_army.append(Mutant(power, strength, family))
        return mutant_army

    return mutant_generator
