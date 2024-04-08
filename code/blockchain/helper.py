import random
import string

# Generates a random string
def generate_random_string(length):
    # The set of characters to choose from
    characters = string.ascii_letters + string.digits

    #Creating the random string
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

# Generate a random binary string
def generate_random_binary_string(length):
    # Generate a list of random binary digits (0 or 1) of the specified length
    binary_digits = [random.choice('01') for _ in range(length)]
    
    # Join the list of binary digits into a string
    binary_string = ''.join(binary_digits)
    
    return binary_string