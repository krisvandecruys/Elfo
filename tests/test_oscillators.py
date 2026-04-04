import math
import time

import matplotlib.pyplot as plt
import numpy as np

from elfo.oscillators import sawtooth, sine, square, triangle, s_and_h

FREQUENCY = 2.0  # Hz
DURATION = 2.0  # seconds
INTERVAL = 0.04  # seconds between samples (~25fps)


def _sample(osc, duration: float, interval: float) -> tuple[list[float], list[float]]:
    """Sample an oscillator at regular intervals.

    Returns elapsed times and values, with t=0 at the first sample.
    The first sample is taken immediately so the LFO's internal start and
    the plot's t=0 are as close as possible.
    """
    raw: list[tuple[float, float]] = []
    deadline = time.perf_counter() + duration
    while True:
        t = time.perf_counter()
        raw.append((t, next(osc)))
        remaining = deadline - time.perf_counter()
        if remaining <= 0:
            break
        time.sleep(min(interval, remaining))

    t0 = raw[0][0]
    times = [t - t0 for t, _ in raw]
    values = [v for _, v in raw]
    return times, values


def _theoretical_sine(t: np.ndarray, f: float) -> np.ndarray:
    return np.sin(2 * math.pi * f * t)


def _theoretical_square(t: np.ndarray, f: float) -> np.ndarray:
    phase = (t * f) % 1.0
    return np.where(phase < 0.5, 1.0, -1.0)


def _theoretical_sawtooth(t: np.ndarray, f: float) -> np.ndarray:
    return (t * f % 1.0) * 2.0 - 1.0


def _theoretical_triangle(t: np.ndarray, f: float) -> np.ndarray:
    phase = (t * f) % 1.0
    return 1.0 - np.abs(phase - 0.5) * 4.0


def _plot(
    ax: plt.Axes,
    title: str,
    t_curve: np.ndarray,
    curve: np.ndarray,
    times: list[float],
    values: list[float],
    step: bool = False,
) -> None:
    if step:
        ax.step(
            t_curve, curve, where="post", color="steelblue", alpha=0.6, label="Expected"
        )
    else:
        ax.plot(t_curve, curve, color="steelblue", alpha=0.6, label="Expected")
    ax.scatter(times, values, color="tomato", zorder=5, s=20, label="LFO samples")
    ax.set_title(title)
    ax.set_ylim(-1.3, 1.3)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Value")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)


def test_sine() -> None:
    times, values = _sample(sine(FREQUENCY), DURATION, INTERVAL)
    t = np.linspace(0, DURATION, 2000)
    fig, ax = plt.subplots(figsize=(10, 3))
    _plot(
        ax, f"Sine — {FREQUENCY} Hz", t, _theoretical_sine(t, FREQUENCY), times, values
    )
    fig.tight_layout()
    plt.show()


def test_square() -> None:
    times, values = _sample(square(FREQUENCY), DURATION, INTERVAL)
    t = np.linspace(0, DURATION, 2000)
    fig, ax = plt.subplots(figsize=(10, 3))
    _plot(
        ax,
        f"Square — {FREQUENCY} Hz",
        t,
        _theoretical_square(t, FREQUENCY),
        times,
        values,
    )
    fig.tight_layout()
    plt.show()


def test_sawtooth() -> None:
    times, values = _sample(sawtooth(FREQUENCY), DURATION, INTERVAL)
    t = np.linspace(0, DURATION, 2000)
    fig, ax = plt.subplots(figsize=(10, 3))
    _plot(
        ax,
        f"Sawtooth — {FREQUENCY} Hz",
        t,
        _theoretical_sawtooth(t, FREQUENCY),
        times,
        values,
    )
    fig.tight_layout()
    plt.show()


def test_triangle() -> None:
    times, values = _sample(triangle(FREQUENCY), DURATION, INTERVAL)
    t = np.linspace(0, DURATION, 2000)
    fig, ax = plt.subplots(figsize=(10, 3))
    _plot(
        ax,
        f"Triangle — {FREQUENCY} Hz",
        t,
        _theoretical_triangle(t, FREQUENCY),
        times,
        values,
    )
    fig.tight_layout()
    plt.show()


def test_s_and_h() -> None:
    """For S&H the expected curve is unknown, so we reconstruct it from
    the samples themselves and verify the dots sit exactly on the steps."""
    times, values = _sample(s_and_h(FREQUENCY), DURATION, INTERVAL)

    # Build a step curve from the samples: value holds until it changes.
    step_times = [0.0]
    step_values = [values[0]]
    for i in range(1, len(values)):
        if values[i] != values[i - 1]:
            step_times.append(times[i])
            step_values.append(values[i])
    step_times.append(DURATION)
    step_values.append(step_values[-1])

    fig, ax = plt.subplots(figsize=(10, 3))
    _plot(
        ax,
        f"S&H (Random) — {FREQUENCY} Hz",
        np.array(step_times),
        np.array(step_values),
        times,
        values,
        step=True,
    )
    fig.tight_layout()
    plt.show()


def test_all() -> None:
    """Show all oscillators in a single figure."""
    fig, axes = plt.subplots(5, 1, figsize=(12, 14))
    t = np.linspace(0, DURATION, 2000)

    specs = [
        ("Sine", sine(FREQUENCY), _theoretical_sine, False),
        ("Square", square(FREQUENCY), _theoretical_square, False),
        ("Sawtooth", sawtooth(FREQUENCY), _theoretical_sawtooth, False),
        ("Triangle", triangle(FREQUENCY), _theoretical_triangle, False),
    ]

    for ax, (name, osc, theory_fn, _step) in zip(axes[:4], specs):
        times, values = _sample(osc, DURATION, INTERVAL)
        _plot(ax, f"{name} — {FREQUENCY} Hz", t, theory_fn(t, FREQUENCY), times, values)

    # Random
    times, values = _sample(s_and_h(FREQUENCY), DURATION, INTERVAL)
    step_times = [0.0]
    step_values = [values[0]]
    for i in range(1, len(values)):
        if values[i] != values[i - 1]:
            step_times.append(times[i])
            step_values.append(values[i])
    step_times.append(DURATION)
    step_values.append(step_values[-1])
    _plot(
        axes[4],
        f"Random (S&H) — {FREQUENCY} Hz",
        np.array(step_times),
        np.array(step_values),
        times,
        values,
        step=True,
    )

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    test_all()
