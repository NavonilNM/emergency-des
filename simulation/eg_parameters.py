class Parameters:
    """
    Parameter class.

    Attributes
    ----------
    interarrival_time : float
        Mean time between arrivals (minutes).
    consultation_time : float
        Mean length of doctor's consultation (minutes).
    number_of_doctors : int
        Number of doctors.
    run_length : int
        Total duration of simulation (minutes).
    verbose : bool
        Whether to print messages as simulation runs.
    log_to_console : bool
        Whether to print activity log to console.
    log_to_file : bool
        Whether to save activity log to file.
    file_path : str
        Path to save log to file.

    -- Output Analysis --
    warm_up_period : int
        Duration of the warm-up period (minutes).
    data_collection_period : int
        Duration of the data collection period (minutes).
    """
    # def __init__(
    #     self, interarrival_time=5, consultation_time=10, number_of_doctors=3, run_length=50, verbose=True
    # ):

  

    # This part of the code is for the section RAP - Model Building  
    # def __init__(
    #     self, interarrival_time=5, consultation_time=10, number_of_doctors=3, run_length=50,
    #     log_to_console=False, log_to_file=False, file_path=None
    # ):
    #     """
    #     Initialise Parameters instance.

    #     Parameters
    #     ----------
    #     dist_config : dict
    #         Holds all distribution specifications.
    #     consultation_time : float
    #         Length of consultation (minutes).
    #     number_of_doctors : int
    #         Number of doctors.
    #     interarrival_time : float
    #         Time between arrivals (minutes).
    #     run_length : int
    #         Total duration of simulation (minutes).
    #     verbose : bool
    #         Whether to print messages as simulation runs.
    #     log_to_console : bool
    #         Whether to print activity log to console.
    #     log_to_file : bool
    #         Whether to save activity log to file.
    #     file_path : str
    #         Path to save log to file.
    #     """
    #     #RAP book - Model building - entity generation
    #     self.dist_config = {
    #         "interarrival_time": {
    #             "class_name": "Exponential",
    #             "params": {"mean": interarrival_time}
    #         }
    #     }

    #     self.interarrival_time = interarrival_time
    #     self.consultation_time = consultation_time
    #     self.number_of_doctors = number_of_doctors
    #     self.run_length = run_length
    #     #self.verbose = verbose
    #     self.log_to_console = log_to_console
    #     self.log_to_file = log_to_file
    #     self.file_path = file_path

   # This part of the code is for the section RAP - Output Analysis  
    def __init__(
        self, interarrival_time=5, consultation_time=10,
        number_of_doctors=3, warm_up_period=30, data_collection_period=40,
        verbose=True
    ):
        """
        Initialise Parameters instance.

        Parameters
        ----------
        interarrival_time : float
            Time between arrivals (minutes).
        consultation_time : float
            Length of consultation (minutes).
        number_of_doctors : int
            Number of doctors.
        warm_up_period : int
            Duration of the warm-up period (minutes).
        data_collection_period : int
            Duration of the data collection period (minutes).
        verbose : bool
            Whether to print messages as simulation runs.
        """
        self.interarrival_time = interarrival_time
        self.consultation_time = consultation_time
        self.number_of_doctors = number_of_doctors
        self.warm_up_period = warm_up_period
        self.data_collection_period = data_collection_period
        self.verbose = verbose