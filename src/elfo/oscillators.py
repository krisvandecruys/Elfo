import math
import random as _random
import time
from collections.abc import Generator


def sine(frequency: float) -> Generator[float, None, None]:
    """Sine wave LFO. Yields values in [-1, +1].

    Args:
        frequency: Frequency in Hz.
    """
    start = time.perf_counter()
    while True:
        yield math.sin(2 * math.pi * (time.perf_counter() - start) * frequency)


def square(frequency: float) -> Generator[float, None, None]:
    """Square wave LFO. Yields +1 or -1.

    Args:
        frequency: Frequency in Hz.
    """
    start = time.perf_counter()
    while True:
        yield (
            1.0
            if (phase := ((time.perf_counter() - start) * frequency) % 1.0) < 0.5
            else -1.0
        )


def sawtooth(frequency: float) -> Generator[float, None, None]:
    """Sawtooth wave LFO. Ramps from +1 to -1 over each cycle.

    Args:
        frequency: Frequency in Hz.
    """
    start = time.perf_counter()
    while True:
        yield -((time.perf_counter() - start) * frequency % 1.0) * 2.0 + 1.0


def triangle(frequency: float) -> Generator[float, None, None]:
    """Triangle wave LFO. Yields values in [-1, +1].

    Args:
        frequency: Frequency in Hz.
    """
    start = time.perf_counter()
    while True:
        yield (
            1.0
            - abs((phase := ((time.perf_counter() - start) * frequency) % 1.0) - 0.5)
            * 4.0
        )


def s_and_h(frequency: float) -> Generator[float, None, None]:
    """Sample-and-hold LFO. Holds a random value for each cycle.

    Args:
        frequency: Frequency in Hz.
    """
    start = time.perf_counter()
    current_step = -1
    current_value = 0.0
    while True:
        if (step := int((time.perf_counter() - start) * frequency)) != current_step:
            current_step = step
            current_value = _random.uniform(-1.0, 1.0)
        yield current_value
