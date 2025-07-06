"""Core simulation model functionality."""


def run_simulation(duration=100):
    """
    Run a simple dummy simulation for the specified duration.

    Parameters
    ----------
    duration: int
        The length of time to run the simulation.

    Returns:
        dict:
            Dummy simulation results.
    """
    return {
        "duration": duration,
        "status": "completed",
        "results": [i for i in range(duration) if i % 10 == 0]
    }