from IPython.display import display
import pandas as pd

from simulation.parameters import (
    ASUArrivals, RehabArrivals, ASULOS, RehabLOS,
    ASURouting, RehabRouting, Param
)

def init_param_class(df, unit, parameter, param_class):
    """
    Instantiate a parameter class using values from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with columns "unit", "parameter", "type", "mean" and "sd".
    unit : str
        Unit name to filter by ("asu" or "rehab").
    parameter : str
        Parameter name to filter by ("iat", "los" or "routing").
    param_class: class
        Class to instantiate.

    Returns
    -------
    object
        An instance of param_class initialised with parameters from the
        DataFrame.
    """
    # Filter data to the specified unit and parameter
    df_subset = df[(df["unit"] == unit) & (df["parameter"] == parameter)]

    # If all SD values are missing, create a dict: {type: mean}
    if df_subset["sd"].isnull().all():
        param_dict = df_subset.set_index("type")["mean"].to_dict()
    # Otherwise, create a nested dict with mean and SD for each type
    else:
        param_dict = {}
        for _, row in df_subset.iterrows():
            param_dict[f"{row["type"]}_mean"] = row["mean"]
            param_dict[f"{row["type"]}_sd"] = row["sd"]

    # Instantiate parameter class using dict
    return param_class(**param_dict)



def setup_param_from_csv(csv_path):
    """
    Create a Param instance using parameter values loaded from a CSV file.

    Parameters
    ----------
    csv_path : str
        Path to csv file containing the parameters. Should have columns "unit",
        "parameter", "type", "mean" and "sd". Missing values should be marked
        as "NA".

    Returns
    -------
    Param
        An instance of Param initialised with the parameters from the CSV file.
    """
    # Load parameter data from CSV, treating "NA" as missing values
    df = pd.read_csv(csv_path, na_values=["NA"])

    # Specify mapping of Param() arguments to their corresponding units,
    # parameter types, and parameter classes
    param_specs = [
        ("asu_arrivals", "asu", "iat", ASUArrivals),
        ("rehab_arrivals", "rehab", "iat", RehabArrivals),
        ("asu_los", "asu", "los", ASULOS),
        ("rehab_los", "rehab", "los", RehabLOS),
        ("asu_routing", "asu", "routing", ASURouting),
        ("rehab_routing", "rehab", "routing", RehabRouting),
    ]

    # Instantiate each parameter class and store in a dictionary
    param_kwargs = {
        name: init_param_class(
            df=df, unit=unit, parameter=parameter, param_class=param_class)
        for name, unit, parameter, param_class in param_specs
    }

    # Return a Param instance initialised with all parameter classes
    return Param(**param_kwargs)



# Defining the main function
def main():
    display(setup_param_from_csv(csv_path="data/parametersNM.csv").__dict__)


# Code entry point
# This ensures that the main function is called when the script is executed
if __name__ == "__main__":
    main()

