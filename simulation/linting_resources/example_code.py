def estimate_wait_time(queue_length, avg_service_time):
    """
    Estimate the total wait time in a queue.
    Parameters
    ----------
    queue_length : int
        Number of people currently ahead in the queue.
    avg_service_time : float
        Average service time per person.
    Returns
    -------
    float
        Estimated total wait time.
    """
    return queue_length * avg_service_time


# There are 4 patients ahead, average service time is 15 minutes
print(estimate_wait_time(queue_length=4, avg_service_time=15))
