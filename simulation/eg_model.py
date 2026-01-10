import simpy
import numpy as np
from simulation.eg_parameters import Parameters
from simulation.eg_patient import Patient
from simulation.eg_simlogger import SimLogger
from sim_tools.distributions import Exponential, Normal, DistributionRegistry

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
    doctor : simpy.Resource
        SimPy resource representing doctors.
    patients : list
        List of Patient objects.
    results_list : list
        List of dictionaries with the attributes of each patient.
    arrival_dist : Exponential
        Distribution used to generate random patient inter-arrival times.
    consult_dist : Exponential
        Distribution used to generate length of a doctor's consultation.
    logger : SimLogger
        The logging instance used for logging messages.
    doctor_time_used : float
        Total time that doctor resources were used for (minutes).
    doctor_time_used_correction : float
        Adjustment for doctor time. Without this, usage is underestimated
        since patients whose consultations began in warm-up but ended
        during data collection are excluded.
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

        # Create resource
        self.doctor = simpy.Resource(
            self.env, capacity=self.param.number_of_doctors
        )

        # Create a random seed sequence based on the run number
        ss = np.random.SeedSequence(self.run_number)
        seeds = ss.spawn(2)

        # Set up attributes to store results
        self.patients = []
        self.results_list = []
        self.doctor_time_used = 0
        self.doctor_time_used_correction = 0

        # Initialise distributions
        self.arrival_dist = Exponential(
            mean=self.param.interarrival_time,
            random_seed=seeds[0]
        )
        self.consult_dist = Exponential(
            mean=self.param.consultation_time,
            random_seed=seeds[1]
        )

        # # Create all the distributions
        # self.dist = DistributionRegistry.create_batch(
        #     config=dict(self.param.dist_config), main_seed=self.run_number
        # )
        # if self.param.verbose:
        #     print(self.dist)

        # Initialise logger
        #self.logger = SimLogger(verbose=self.param.verbose)

        # # This part of the code is for the section RAP - Model Building
        # self.logger = SimLogger(log_to_console=self.param.log_to_console,
        #                         log_to_file=self.param.log_to_file,
        #                         file_path=self.param.file_path)
        # self.logger.log(sim_time=self.env.now, msg="Initialise model:")
        # self.logger.log(vars(self))
        # self.logger.log(sim_time=self.env.now, msg="Parameters:")
        # self.logger.log(vars(self.param))
            

    # # This part of the code is for the section RAP - Model Building  
    # def generate_arrivals(self):
    #     """
    #     Process that generates patient arrivals.
    #     """
    #     while True:
    #         # Sample and pass time to next arrival
    #         sampled_iat = self.arrival_dist.sample()
    #         #sampled_iat = self.dist["interarrival_time"].sample()
    #         yield self.env.timeout(sampled_iat)

    #         # Create a new patient
    #         patient = Patient(patient_id=len(self.patients)+1,
    #                           arrival_time=self.env.now)
    #         self.patients.append(patient)

    #         # Log arrival time
    #         self.logger.log(msg=f"Patient {patient.patient_id} arrives.",
    #                         sim_time=self.env.now)

    #         # # Print arrival time
    #         # if self.param.verbose:
    #         #     print(f"Patient {patient.patient_id} arrives " +
    #         #           f"at time: {patient.arrival_time:.3f}")
            
    #         # Start process of consultation
    #         self.env.process(self.consultation(patient))


    # This part of the code is for the section RAP - Output Analysis 
    def generate_arrivals(self):
        """
        Process that generates patient arrivals.
        """
        while True:
            # Sample and pass time to next arrival
            sampled_iat = self.arrival_dist.sample()
            yield self.env.timeout(sampled_iat)

            # Check whether arrived during warm-up or data collection
            if self.env.now < self.param.warm_up_period:
                period = "\U0001F538 WU"
            else:
                period = "\U0001F539 DC"

            # Create a new patient
            patient = Patient(patient_id=len(self.patients)+1,
                              period=period,
                              arrival_time=self.env.now)
            self.patients.append(patient)

            # Print arrival time
            if self.param.verbose:
                print(f"{patient.period} Patient {patient.patient_id} " +
                      f"arrives at time: {patient.arrival_time:.3f}")

            # Start process of consultation
            self.env.process(self.consultation(patient))            


    def consultation(self, patient):
        """
        Process that simulates a consultation.

        Parameters
        ----------
        patient :
            Instance of the Patient() class representing a single patient.
        """
        start_wait = self.env.now

        # Patient requests access to a doctor (resource)
        with self.doctor.request() as req:
            yield req

            # # Log consultation start time
            # self.logger.log(
            #     msg=f"Patient {patient.patient_id} starts consultation.",
            #     sim_time=self.env.now
            # )

            # Record how long patient waited before consultation
            patient.wait_time = self.env.now - start_wait

            if self.param.verbose:
                print(f"{patient.period} Patient {patient.patient_id} starts consultation " +
                      f"at: {self.env.now:.3f}")

            # Sample consultation duration and pass time spent with doctor
            patient.time_with_doctor = self.consult_dist.sample()
            
            
            # Add to total doctor time used
            # If it runs past simulation end, only count the time until end
            remaining_time = (
                self.param.warm_up_period +
                self.param.data_collection_period) - self.env.now
            self.doctor_time_used += min(
                patient.time_with_doctor, remaining_time)

            
            # During warm-up: check if consultation continues past warm-up.
            # If so, record the portion overlapping with data collection in
            # doctor_time_used_correction (capped at the simulation end).
            remaining_warmup = self.param.warm_up_period - self.env.now
            if remaining_warmup > 0:
                time_exceeding_warmup = patient.time_with_doctor - remaining_warmup
                if time_exceeding_warmup > 0:
                    self.doctor_time_used_correction += min(
                        time_exceeding_warmup,
                        self.param.data_collection_period)

            
            # Pass time spent with the doctor
            yield self.env.timeout(patient.time_with_doctor)

            # Record end time
            if self.param.verbose:
                print(f"{patient.period} Patient {patient.patient_id} " +
                      f"leaves at: {self.env.now:.3f}")

    # This part of the code is for the section RAP - Model Building  
    # def run(self):
    #     """
    #     Run the simulation.
    #     """
    #     # Schedule arrival generator
    #     self.env.process(self.generate_arrivals())

    #     # Run the simulation
    #     self.env.run(until=self.param.run_length)



    # This part of the code is for the section RAP - Output Analysis 
    def reset_results(self):
        """
        Reset results.
        """
        self.patients = []
        self.doctor_time_used = 0

    def warmup(self):
        """
        Reset result collection after the warm-up period.
        """
        if self.param.warm_up_period > 0:
            # Delay process until warm-up period has completed
            yield self.env.timeout(self.param.warm_up_period)
            # Reset results variables
            self.reset_results()
            if self.param.verbose:
                print(f"Warm up period ended at time: {self.env.now}")
        
            # Add correction for patients whose consultations began in
            # warm-up but continued into data collection.
            self.doctor_time_used += self.doctor_time_used_correction


    def run(self):
        """
        Run the simulation.
        """
        # Schedule arrival generator and warm-up
        self.env.process(self.generate_arrivals())
        self.env.process(self.warmup())

        # Run the simulation
        self.env.run(until=(self.param.warm_up_period +
                            self.param.data_collection_period))
        
        # Create list of dictionaries containing each patient's attributes
        self.results_list = [x.__dict__ for x in self.patients]