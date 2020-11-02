
import logging

def exception_handler(function):
    """
    Wrap the function passed in and log exceptions if they occur. 

    Parameters
    ----------
    function : object
        A user-defined function.  

    Returns
    -------
    wrapper : object
        If an exception occurs, display a log with a traceback 
        of the error.  
    """
    def wrapper(*args, **kwargs):
        try:
            #  call the function 
            return function(*args, **kwargs)
        except Exception as error:
            #  log the exception 
            logging.exception(error)
            print("Code failed.")
    return wrapper