import logging

log = logging.getLogger()

log.setLevel(logging.INFO)
logging_format = logging.Formatter('[%(asctime)s | %(name)s | %(levelname)s]: %(message)s', "%Y-%m-%d %p %I:%M:%S")

command = logging.StreamHandler()
command.setFormatter(logging_format)

log.addHandler(command)
