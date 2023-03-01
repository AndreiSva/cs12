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
    players = list(map(
        lambda player :
            sqrt((x - player["x"])**2 - (y - player["y"])**2) <= radius,
        party))
    for i in range(len(players)):
        if players[i] == True:
            party[i]["inventory"].append("candy")

def lists_to_dict(list1, list2):
    """Takes in a list of keys and values and combines
    them into a dictionary"""
    d = {}
    for i in range(len(list1)):
        d[list1[i]] = list2[i]
    return d

def is_prime(n):
    """Returns True if n is a prime number"""
    for i in range(2, n - 1):
        if n % i == 0:
            return False
    return True

primes = []

def prime_factor(n):
    def pfactor(num):
        print(num)
        if num == []:
            return None
        
        factors = []
        for x in num:
            i = 2
            while i < x:
                if x % i == 0:
                    factors += pfactor([i])
                    x //= i
                i += 1
        print(factors)
        return factors
    print(pfactor([n]))
        
