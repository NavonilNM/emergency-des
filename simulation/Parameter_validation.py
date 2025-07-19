# pylint: disable=missing-module-docstring

# def param_function(transfer_prob=0.3):
#     """
#     Returns transfer_prob for validation example.

#     Parameters
#     ----------
#     transfer_prob : float
#         Transfer probability (0-1).

#     Returns
#     -------
#     Dictionary containing the transfer_prob parameter.
#     """
#     return {"transfer_prob": transfer_prob}

# # pylint: disable=undefined-variable
# # Use function to create params dict
# params = param_function()

# # Mistype transfer_prob
# params["transfer_probs"] = 0.4
# print(params)

# ---

# # Nav example of using a class with __slots__
# class Params:
#     __slots__ = ['transfer_prob']
#     def __init__(self, transfer_prob):
#         self.transfer_prob = transfer_prob
    
#     def __repr__(self): 
#         return f"Params(transfer_prob={self.transfer_prob})"

# # Defining the main function
# def main():
#     params = Params(0.3)
#     params.transfer_prob = 0.4  # This is OK
#     params.transfer_probs = 0.7 #This leads to AttributeError
#     print(params)

# # Code entry point
# if __name__ == "__main__":
#     main()

# ---

# Parameter validation within the model functions
# pylint: disable=missing-module-docstring

transfer_prob = 0 #Global variable

def param_function(transfer_prob=0.3):
    return {"transfer_prob": transfer_prob}

def validate_param(parameters):
    local_transfer_prob = parameters["transfer_prob"]
    if local_transfer_prob < 0 or local_transfer_prob > 1:
        raise ValueError(
          f"transfer_prob must be between 0 and 1, but is: {local_transfer_prob}"
        )
    else:
        print(f"transfer_prob is valid: {local_transfer_prob}")
        # Update global variable
        global transfer_prob
        transfer_prob=local_transfer_prob
    
def model(param_dict):
    validate_param(parameters=param_dict)


param = param_function(transfer_prob = 0.4)
try:
    model(param)
except ValueError as e:
    print(e)

print(transfer_prob)