import simpy
import numpy as np
from sim_tools.distributions import Exponential, Normal, DistributionRegistry



class Parameters:
    """
    Parameter class.

    Attributes
    ----------
    interarrival_time : float
        Mean time between arrivals (minutes).
    run_length : int
        Total duration of simulation (minutes).
    verbose : bool
        Whether to print messages as simulation runs.
    """
    def __init__(
        self, interarrival_time=5, run_length=50, verbose=True
    ):
        """
        Initialise Parameters instance.

        Parameters
        ----------
        dist_config : dict
            Holds all distribution specifications.
        interarrival_time : float
            Time between arrivals (minutes).
        run_length : int
            Total duration of simulation (minutes).
        verbose : bool
            Whether to print messages as simulation runs.
        """
        self.dist_config = {
            "interarrival_time": {
                "class_name": "Exponential",
                "params": {"mean": interarrival_time}
            }
        }
        self.interarrival_time = interarrival_time
        self.run_length = run_length
        self.verbose = verbose


class Patient:
    """
    Represents a patient.

    Attributes
    ----------
    patient_id : int
        Unique patient identifier.
    arrival_time : float
        Time patient entered the system (minutes).
    """
    def __init__(self, patient_id, arrival_time):
        """
        Initialises a new patient.

        Parameters
        ----------
        patient_id : int
            Unique patient identifier.
        arrival_time : float
            Time patient entered the system (minutes).
        """
        self.patient_id = patient_id
        self.arrival_time = arrival_time

class Model:
    """
    Simulation model.

    Attributes
    ----------
    param : Parameters
        Simulation parameters.
    run_number : int
        Run number for random seed generation.
    env : simpy.Environment
        The SimPy environment for the simulation.
    patients : list
        List of Patient objects.
    arrival_dist : Exponential
        Distribution used to generate random patient inter-arrival times.
    """
    def __init__(self, param, run_number):
        """
        Create a new Model instance.

        Parameters
        ----------
        param : Parameters
            Simulation parameters.
        run_number : int
            Run number for random seed generation.
        """
        self.param = param
        self.run_number = run_number

        # Create SimPy environment
        self.env = simpy.Environment()

        # # Create a random seed sequence based on the run number
        # ss = np.random.SeedSequence(self.run_number)
        # seeds = ss.spawn(1)

        # Set up attributes to store results
        self.patients = []

        # # Initialise distributions
        # self.arrival_dist = Exponential(
        #     mean=self.param.interarrival_time,
        #     random_seed=seeds[0]
        # )

        # Create all the distributions
        self.dist = DistributionRegistry.create_batch(
            config=dict(self.param.dist_config), main_seed=self.run_number
        )
        if self.param.verbose:
            print(self.dist)
            


    def generate_arrivals(self):
        """
        Process that generates patient arrivals.
        """
        while True:
            # Sample and pass time to next arrival
            #sampled_iat = self.arrival_dist.sample()
            sampled_iat = self.dist["interarrival_time"].sample()
            yield self.env.timeout(sampled_iat)

            # Create a new patient
            patient = Patient(patient_id=len(self.patients)+1,
                              arrival_time=self.env.now)
            self.patients.append(patient)

            # Print arrival time
            if self.param.verbose:
                print(f"Patient {patient.patient_id} arrives " +
                      f"at time: {patient.arrival_time:.3f}")

    def run(self):
        """
        Run the simulation.
        """
        # Schedule arrival generator
        self.env.process(self.generate_arrivals())

        # Run the simulation
        self.env.run(until=self.param.run_length)


# Defining the main function
def main():
    param = Parameters()
    model = Model(param=param, run_number=0)
    model.run()
    

# Code entry point
# This ensures that the main function is called when the script is executed
if __name__ == "__main__":
    main()
