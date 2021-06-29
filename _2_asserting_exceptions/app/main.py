def enter_the_pub(age:int) -> None :
    if (age < 18) :
        raise ValueError("Consuming Alcohol is not permitted under 18 years old")