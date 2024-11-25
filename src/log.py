# Setup the root logger
import logging


LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)

# Create a console handler (prints logs to terminal)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the console handler
console_handler_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(console_handler_formatter)

# Add the console handler to the logger
LOG.addHandler(console_handler)
