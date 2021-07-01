from dataclasses import dataclass


@dataclass
class Person:
    age: int
    name: str


def check_person_age(person: Person):
    if person.age < 18:
        print("You are under 18")
    else :
        print("You can vote, you are an adult")
