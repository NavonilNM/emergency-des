from simulation.eg_parameters import Parameters
from simulation.eg_runner_usingMonitoredResource import RunnerMR

param = Parameters(
    interarrival_time=5,
    consultation_time=10,
    number_of_doctors=3,
    warm_up_period=30,
    data_collection_period=40,
    number_of_runs=5,
    verbose=False
)

runner = RunnerMR(param=param)
results = runner.run_reps()
results["patient"].to_csv("simulation/tests_resources/python_patient.csv", index=False)
results["run"].to_csv("simulation/tests_resources/python_run.csv", index=False)
results["overall"].to_csv("simulation/tests_resources/python_overall.csv", index=False)