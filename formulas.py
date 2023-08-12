import sys

def add(values: list) -> float:
    '''
    Sums up all values in input list.
    '''
    sum = 0
    for val in values:
        sum += float(val)
    return sum

def subtract(values: list) -> float:
    '''
    Takes the first value then subtracts the rest of the values in the list.
    '''
    total = values[0]
    for val in values[1:]:
        total = total - val
    return total

def multiply(values: list) -> float:
    '''
    Prods all the values in input list.
    '''
    product = 1
    for val in values:
        product = float(val) * product
    return product

def modulo(values: list) -> float:
    '''
    a mod b where a is position 0 and b is position 1 in the input list.
    '''
    return values[0] % values[1]

def divide(values: list) -> float:
    '''
    Divides the first value in the list by every other value
    '''
    total, denom = values[0], values[1:]
    for divisor in denom:
        total = total / divisor
    return total

def exponent(values) -> float:
    '''
    a^b where a is position 0 and b is position 1 in the input list.
    '''
    return float(values[0])**( float(values[1]) )

if __name__ == "__main__":
    exit()