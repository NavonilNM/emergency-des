# Paramater file for simulation
# Import required packages
import pandas as pd

# Import and preview parameter file
# data = pd.read_csv("data/parameters.csv")
# print(data)

# 1. Define Parameter class
class Parameters:  # pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-positional-arguments, too-few-public-methods
    """
    Container for simulation parameters across patient demographics.
    """
    def __init__(
        self,
        adult_interarrival, adult_consultation, adult_transfer,
        child_interarrival, child_consultation, child_transfer,
        elderly_interarrival, elderly_consultation, elderly_transfer
    ):
        """
        Initialise Parameters instance.

        Parameters
        ----------
        adult_interarrival : float
            Time between adult patient arrivals (e.g., in minutes or hours).
        adult_consultation : float  
            Duration of consultation time for adult patients.
        adult_transfer : float
            Time required to transfer adult patients between stages.
        child_interarrival : float
            Time between child patient arrivals (e.g., in minutes or hours).
        child_consultation : float
            Duration of consultation time for child patients.
        child_transfer : float
            Time required to transfer child patients between stages.
        elderly_interarrival : float
            Time between elderly patient arrivals (e.g., in minutes or hours).
        elderly_consultation : float
            Duration of consultation time for elderly patients.
        elderly_transfer : float
            Time required to transfer elderly patients between stages.
        """
        # Adult parameters
        self.adult_interarrival = adult_interarrival
        self.adult_consultation = adult_consultation
        self.adult_transfer = adult_transfer
        # Child parameters
        self.child_interarrival = child_interarrival
        self.child_consultation = child_consultation
        self.child_transfer = child_transfer
        # Elderly parameters
        self.elderly_interarrival = elderly_interarrival
        self.elderly_consultation = elderly_consultation
        self.elderly_transfer = elderly_transfer


# 2. Helper function to import parameters
def setup_param_from_csv(csv_path):
    """
    Create a Parameters instance using parameter values loaded from a CSV file.

    Parameters
    ----------
    csv_path : str
        Path to CSV file containing the parameters. Should have columns
        "patient", "metric", and "value".

    Returns
    -------
    Parameters
        Instance of Parameters initialised with parameters from the CSV file.
    """

    # Import the parameters
    param_file = pd.read_csv(csv_path)

    # Create name-value mappings
    values = {
      f"{row.patient}_{row.metric}": row.value
      for row in param_file.itertuples()
    }

    # Pass these values to the Parameters class
    return Parameters(**values)


# 3. Load and use parameters
# Import parameters
params = setup_param_from_csv("data/example_parameters.csv")

# View object
print(params.__dict__)