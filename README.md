# Elfo

> You'll be amazed how much fun I am on my own.

A minimal Python library of **Low Frequency Oscillators** (LFOs).

Each oscillator is a generator that yields `float` values in the range `[-1.0, +1.0]`. The phase is computed from real wall-clock time (`time.perf_counter`), so values are always temporally accurate regardless of how fast or slow you consume them.

## Oscillators

| Function    | Description                                      |
|-------------|--------------------------------------------------|
| `sine`      | Smooth sinusoidal wave                           |
| `square`    | Jumps between +1 and -1 at the half-cycle point  |
| `sawtooth`  | Linear ramp from -1 to +1, then instant reset    |
| `triangle`  | Linear ramp up then down, no discontinuity       |
| `s_and_h`   | Sample-and-hold: random value held for one cycle |

## Installation

```bash
pip install elfo
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add elfo
```

## Usage

```python
from elfo import sine, square, sawtooth, triangle, s_and_h

# Create an oscillator at 0.5 Hz
lfo = sine(0.5)

# Pull values whenever you need them — phase is always correct
value = next(lfo)   # float in [-1.0, +1.0]
```

The oscillator's internal clock starts at the moment the generator is created. There is no need to pass timestamps — calling `next()` at any point returns the value for that exact instant.

### Applying an LFO to a parameter

```python
import time
from elfo import triangle

base_volume = 0.8
tremolo = triangle(4.0)  # 4 Hz tremolo

while True:
    volume = base_volume + next(tremolo) * 0.2  # ±0.2 around base
    time.sleep(0.01)
```

## Running the visual tests

The `tests/` directory contains plotting tests that sample each oscillator in real time and overlay the dots on the theoretical waveform — they should align.

```bash
uv run python tests/test_oscillators.py
```

## Requirements

- Python ≥ 3.13
- `matplotlib` (only required for the visual tests)
