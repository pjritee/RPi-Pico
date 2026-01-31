# Support for building generators that could, for example, be used to drive PWM LEDs

import sys
import random

# These generators are intended to be generally useful and so for writing the implementation
# we use type hints that would be valid in standard Python. However this is not supported in MicroPython
# so we skip type checking support when running in MicroPython
if sys.implementation.name != "micropython":
    from typing import Generator, TypeVar, Callable 
    #from collections.abc import Callable   

    # declare types for generator functions that returns a generator yielding a value of type T
    T = TypeVar('T')

# The functions below are intended to be used to build up complex generators from simpler ones.
# Several of the functions below repeatedly use one or more generators and we need to use functions
# that return generators rather than the generators themselves so that each time the returned
# function is called a new generator is created. 
# For example if we want to create a generator that repeatedly yields from a sine wave generator
# we need to use a function that returns a sine wave generator rather than the sine wave generator itself
# because once a generator has been exhausted it cannot be reused.
# For uniformity we insist that all the generator functions used do not take any arguments.
# The type hint for such a function is Callable[[], Generator[T,None,None]].
# 
# For convenience we provide a decorator bind_generator_args that can be used to convert
# a generator function that takes arguments into one that takes no arguments by binding
# the supplied arguments. 

# A decorator that converts a generator function with arbitrary arguments into a generator function
# with no arguments by binding the supplied arguments
def bind_generator_args[T](generator_func: Callable[..., Generator[T,None,None]]) -> Callable[[], Generator[T,None,None]]  :
    def decorator(func: Callable[..., Generator[T,None,None]]) -> Callable[[], Generator[T,None,None]]:
        def bound_generator(*args, **targs) -> Callable[[], Generator[T,None,None]]:
            return lambda: func(*args, **targs)  # zero argument function returning the generator
        return bound_generator
    return decorator(generator_func)
    

@bind_generator_args
def sequencer[T](generators: list[Callable[[], Generator[T,None,None]]]) -> Generator[T,None,None]:
    """A function that, when called, returns a generator that iterates through the supplied list of generators,
    yielding from each in turn."""
    for generator in generators:
        yield from generator()

@bind_generator_args
def chooser[T](generators: list[Callable[[], Generator[T,None,None]]]) -> Generator[T,None,None]:
    """A function that, when called, returns a generator that randomly chooses from the supplied list of generators,
    yielding from the chosen generator."""
    yield from random.choice(generators)()

@bind_generator_args
def repeater[T](number: int, generator: Callable[[], Generator[T,None,None]]) -> Generator[T,None,None]:
    """A function that, when called, returns a generator that yields from the supplied generator
    the supplied number of times."""
    for _ in range(number):
        yield from generator()

@bind_generator_args
def random_repeater[T](probability: int, generator: Callable[[], Generator[T,None,None]]) -> Generator[T,None,None]:
    """A function that, when called, returns a generator that yields from the supplied generator
    repeatedly with the supplied probability."""
    while random.randint(0,100) < probability:
        yield from generator()

@bind_generator_args
def always_repeater[T](generator: Callable[[], Generator[T,None,None]]) -> Generator[T,None,None]:
    """A function that, when called, returns a generator that yields from the supplied generator
    forever."""
    while True:
        yield from generator()  

@bind_generator_args
def take_while[T](condition: Callable[[], bool], generator: Callable[[], Generator[T,None,None]]) -> Generator[T,None,None]:
    """A function that, when called, returns a generator that yields from the supplied generator
    while the supplied condition is true."""
    g = generator()
    while condition():
        yield next(g)


# Test code and example usage
if __name__ == "__main__":
    # Simple test generators
    @bind_generator_args
    def constant_gen(value: float) -> Generator[float, None, None]:
        """A simple generator that always yields the same value."""
        while True:
            yield value
    @bind_generator_args
    def ramp_gen(start: float, end: float, steps: int) -> Generator[float, None, None]:
        """A generator that yields values from start to end in steps."""
        step_size = (end - start) / steps
        current = start
        for _ in range(steps):
            yield current
            current += step_size
    @bind_generator_args
    def sine_wave_gen(amplitude: float = 1.0, frequency: float = 1.0, steps: int = 100) -> Generator[float, None, None]:
        """A generator that yields values from a sine wave."""
        import math
        for i in range(steps):
            yield amplitude * math.sin(2 * math.pi * frequency * i / steps)
    
    # Test the generator builders
    print("Testing generator builders...")
    
    # Test sequencer
    print("\n1. Testing sequencer:")
    seq_gen = sequencer([
        constant_gen(1.0),
        ramp_gen(0.0, 1.0, 5),
        constant_gen(0.5)
    ])
    values = []
    for i, val in enumerate(seq_gen()):
        values.append(round(val, 2))
        if len(values) >= 10:  # Limit output
            break
    print(f"Sequencer output: {values}")
    
    # Test chooser
    print("\n2. Testing chooser:")
    choose_gen = chooser([
        constant_gen(1.0),
        constant_gen(2.0),
        constant_gen(3.0)
    ])
    values = []
    for i in range(10):
        val = next(choose_gen())
        values.append(val)
    print(f"Chooser output (10 random choices): {values}")
    
    # Test repeater
    print("\n3. Testing repeater:")
    repeat_gen = repeater(3, ramp_gen(0.0, 1.0, 3))
    values = []
    for val in repeat_gen():
        values.append(round(val, 2))
    print(f"Repeater output (3 times): {values}")
    
    # Test random_repeater
    print("\n4. Testing random_repeater:")
    random_repeat_gen = random_repeater(50, constant_gen(1.0))  # 50% probability
    values = []
    count = 0
    for val in random_repeat_gen():
        values.append(val)
        count += 1
        if count >= 20:  # Safety limit
            break
    print(f"Random repeater output (up to 20 values): {values}")
    
    # Test always_repeater
    print("\n5. Testing always_repeater:")
    always_repeat_gen = always_repeater(constant_gen(42.0))
    values = []
    for i, val in enumerate(always_repeat_gen()):
        values.append(val)
        if i >= 4:  # Only take first 5 values
            break
    print(f"Always repeater output (first 5): {values}")
    
    # Test take_while
    print("\n6. Testing take_while:")
    counter = [0]  # Use list to modify in nested function
    def stopping_condition() -> bool:
        print(counter)
        return counter[0] < 3
    
    take_while_gen = take_while(stopping_condition, constant_gen(1.0))
    values = []
    for val in take_while_gen():
        print(counter[0])
        values.append(val)
        counter[0] += 1
    print(f"Take while output (while counter < 3): {values}")
    
    print("\nAll tests completed!")