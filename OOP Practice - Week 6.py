# OOP Practice - Fraction
## Name: Aya Ben Saghroune
import random
import statistics
import time
import math

class Fraction:
    def __init__(self, numerator, denominator):
        self.num = numerator
        self.den = denominator
    def __str__(self):
        return f"{self.num}/{self.den}"
    def getNumerator(self) -> int:
        return self.num
    def getDenominator(self) -> int:
        return self.den 
    def isImproper(self) -> bool:
        return True if self.getNumerator() > self.getDenominator() else False
    def integerLowerBound(self) -> int:
        value = self.getNumerator() // self.getDenominator()
        return value
    def integerUpperBound(self) -> int:
        return (self.getNumerator() // self.getDenominator())+1 if type(self.getNumerator() % self.getDenominator()) != 0 else (self.getNumerator() / self.getDenominator())

f1 = Fraction(5, 2)
f2 = Fraction(2, 5)

assert f1.integerLowerBound() == 2, "Improper Calculation"
assert f1.integerUpperBound() == 3, "Improper Calculation"

assert f2.integerLowerBound() == 0, "Improper Calculation"
assert f2.integerUpperBound() == 1, "Improper Calculation"
