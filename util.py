import time
import random

def random_wait():
    float(random.randint(0, 1000)) / 1000

def flatten(list_of_lists):
    return reduce(list.__add__, list_of_lists)
