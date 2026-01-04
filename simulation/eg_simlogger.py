
import logging
import os
from pprint import pformat

import numpy as np
from rich.logging import RichHandler
from rich.console import Console
import simpy
from sim_tools.distributions import Exponential

class SimLogger:
    """
    Provides log of events as the simulation runs.

    Attributes
    ----------
    verbose : bool
        Whether to print messages as simulation runs.
    log_to_console : bool
        Whether to print activity log to console.
    log_to_file : bool
        Whether to save activity log to file.
    file_path : str
        Path to save log to file.
    """
    def __init__(self, verbose):
        """
        Initialise logging class.

        Parameters
        ----------
        verbose : bool
            Whether to print messages as simulation runs.
        """
        self.verbose = verbose
        if self.verbose:
            self.logger = logging.getLogger(__name__)
            self._configure_logging()


    def __init__(self, log_to_console, log_to_file, file_path):
        """
        Initialise logging class.

        Parameters
        ----------
        log_to_console : bool
            Whether to print activity log to console.
        log_to_file : bool
            Whether to save activity log to file.
        file_path : str
            Path to save log to file.
        """
        self.log_to_console = log_to_console
        self.log_to_file = log_to_file
        self.file_path = file_path

        # If saving to file, check path is valid
        if self.log_to_file:
            self._validate_log_path()

        if self.log_to_console or self.log_to_file:
            self.logger = logging.getLogger(__name__)
            self._configure_logging()


    def _validate_log_path(self):
        """
        Validate the log file path.

        Raises
        ------
        ValueError
            If log path is invalid.
        """
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            raise ValueError(
                f"The directory '{directory}' for the log file does not exist."
            )
        if not self.file_path.endswith(".log"):
            raise ValueError(
                f"The log file path '{self.file_path}' must end with '.log'."
            )
        

    def _configure_logging(self):
        """
        Configure the logger.
        """
        # Ensure any existing handlers are removed to avoid duplication
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Configure RichHandler without INFO/ERROR labels, times or paths
        # to log message. Set up console with jupyter-specific behaviour
        # disabled to prevent large gaps between each log message on ipynb.
        console = Console()
        console.is_jupyter = False
        rich_handler = RichHandler(
            console=console, show_time=False,
            show_level=False, show_path=False
        )


        # Add handlers to the logger
        handlers = []
        if self.log_to_console:
            handlers.append(rich_handler)
        if self.log_to_file:
            handlers.append(logging.FileHandler(self.file_path, mode="w"))
        for handler in handlers:
            self.logger.addHandler(handler)

        # Add handler to the logger
        #self.logger.addHandler(rich_handler)

        # Set logging level and format. If don't set level info, it would
        # only show log messages which are warning, error or critical.
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
        #rich_handler.setFormatter(formatter)
        for handler in handlers:
            handler.setFormatter(formatter)
    

    def sanitise_object(self, obj):
        """
        Sanitise object references to avoid memory addresses in logs.

        Parameters
        ----------
        obj : object
            Object to sanitise.

        Returns
        -------
        str
            Sanitised version of the object. For basic types (int, float,
            bool, str, list, dict, tuple, set), returns the string
            representation. For other objects, returns the class name in
            angle brackets.
        """
        if isinstance(obj, object) and not isinstance(
            obj, (int, float, bool, str, list, dict, tuple, set)
        ):
            # Return the class name instead of the memory address
            return f"<{obj.__class__.__module__}.{obj.__class__.__name__}>"
        return obj



    def log(self, msg, sim_time=None):
        """
        Log a message if logging is enabled.

        Parameters
        ----------
        msg : str
            Message to log.
        sim_time : float or None, optional
            Current simulation time. If provided, prints before message.
        """

        # Format dictionaries so easier to read
        if isinstance(msg, dict):
            msg = {key: self.sanitise_object(value)
                   for key, value in msg.items()}
            msg = pformat(msg, indent=4)


        # if self.verbose:
        #     if sim_time is not None:
        #         self.logger.info("%0.3f: %s", sim_time, msg)
        #     else:
        #         self.logger.info(msg)
        
        if self.log_to_console or self.log_to_file:
            if sim_time is not None:
                self.logger.info("%0.3f: %s", sim_time, msg)
            else:
                self.logger.info(msg)