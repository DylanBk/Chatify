import logging
from logging.handlers import RotatingFileHandler
import uuid

# --- ERROR LOGGING CONFIG

class ServerError():
    """
    Class to log server errors to a file.
    """
    def __init__(self, message:str, error:Exception):
        """
        Constructor for the ServerError class.
        Parameters:
            message: the message to log
            error: the error to log
        """
        self.id = uuid.uuid4()
        self.message = message
        self.error = error

    def __str__(self):
        """
        String representation of the ServerError class.
        """
        return f"UUID: {self.id} - Message: {self.message} - Error: {self.error}"

def log_error(message:str, error:Exception):
    """
    Function to log errors to a file.
    Parameters:
        message: the message to log
        error: the error to log
    """
    error = ServerError(message, error)
    logger.error(error)

log_handler = RotatingFileHandler('./logs/server-errors.log', maxBytes=1_000_000, backupCount=3)
log_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.addHandler(log_handler)


# --- EVENT LOGGING CONFIG ---

class ServerEvent():
    """
    Class to log server events to a file.
    """
    def __init__(self, message:str, event:any):
        """
        Constructor for the ServerEvent class.
        Parameters:
            message: the message to log
            event: the event to log
        """
        self.id == uuid.uuid4()
        self.message = message
        self.event = event

    def __str__(self):
        """
        String representation of the ServerEvent class.
        """
        return(f"UUID: {self.id} - Message: {self.message} - Event: {self.event}")
    
def log_event(message:str, event:any):
    """
    Function to log events to a file.
    Parameters:
        message: the message to log
        event: the event to log
    """
    event = ServerEvent(message, event)
    logger.info(event)

event_handler = RotatingFileHandler('./logs/server-events.log', maxBytes=1_000_000, backupCount=3)
event_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)