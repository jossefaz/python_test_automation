import enum
from dataclasses import dataclass
from typing import List


class Powers(enum.Enum):
    Ice = "Ice"
    Fire = "Fire"
    Psycho = "PSYCHO"
    Self_recovery = "SELF_RECOVER"


class MutantFamily(enum.Enum):
    Beast = "BEAST"
    Mind = "MIND"
    Daemons = "DAEMONS"
    Angels = "ANGELS"


class MutantStrength(enum.Enum):
    Weak = 1
    Middle = 2
    Strong = 3
    God = 4

    def __gt__(self, other):
        return self.value > other.value


@dataclass
class Mutant:
    power: Powers
    strength: MutantStrength
    family: MutantFamily

    def __str__(self):
        return f"{self.family} has a power of {self.power} and strength {self.strength}"


def fight_mutants(army_of_mutants: List[Mutant]):
    return max(army_of_mutants, key=lambda m: m.strength)
