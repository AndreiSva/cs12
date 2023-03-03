# Assignment 2 Part 1
# Andrei Sova
# 3/03/2023

from math import sqrt

def inventory_size(player):
    """Takes a player dictionary as an argument and
    returns the number of items in their inventory"""

    return len(player["inventory"])

def pinata(x, y, radius, party):
    """Adds 'candy' to any player in 'party' who's x
    coordinates are inside the radius of pinata x y"""
    for player,i in enumerate(len(party)):
        if sqrt((x - player["x"])**2 - (y - player["y"])**2) <= radius:
            party[i]["inventory"].append("candy")

def lists_to_dict(list1, list2):
    """Takes in a list of keys and values and combines
    them into a dictionary"""
    d = {}
    for i in range(len(list1)):
        d[list1[i]] = list2[i]
    return d

primes = []

def is_prime(n):
    """Returns True if n is a prime number"""
    if n in primes:
        return True
    if n % 2 == 0 and n != 2:
        return False
    for i in range(3, n - 1, 2):
        if n % i == 0:
            return False
        primes.append(n)
    return True

def prime_factor(n):
    def __primefactor(num):
        if len(num) == 1 and is_prime(num[0]):
            return num
        factors = []
        for x in num:
            i = 2
            while i < x:
                if x % i == 0:
                    factors += __primefactor([i]) + __primefactor([x // i])
                    break
                i += 1
        return factors
    return __primefactor([n])
