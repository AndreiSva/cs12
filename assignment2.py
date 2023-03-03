# Assignment 2 Part 2
# Andrei Sova
# 3/03/2023

class Binomial:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __add__(self, other):
        """returns a new binomial object that is the sum of this one and other"""
        return Binomial(self.a + other.a, self.b + other.b)
    def __sub__(self, other):
        """returns a new binomial object that is the difference of this one and other"""
        return Binomial(self.a - other.a, self.b - other.b)
    def __eq__(self, other):
        """returns true if other and this object have the same value"""
        return self.a == other.a and self.b == other.b
    def __str__(self):
        """returns a string representation of the binomial"""
        return ("-" if self.a < 0 else "") + (str(self.a) if abs(self.a) > 1 else "") + "x" + ("+" if self.b > 0 else "-") + str(abs(self.b))
    def eval(self, x):
        """evaluates the binomial for the value x"""
        return self.a * x + self.b
    def solve(self, other):
        """solves for x given another binomial object"""
        return (other.b - self.b) // (self.a - other.a)

class Polynomial:
    terms: list
