import logging
import os

root_log_level = getattr(logging, os.environ.get('ROOT_LOG_LEVEL') or 'DEBUG')

format = '%(levelname)s: %(name)s - %(message)s'

# AWS Lambda adds the timestamp to all logs
if not os.getenv('LAMBDA_TASK_ROOT'):
    format = "%(asctime)s " + format

# The Lambda environment pre-configures a handler logging to stderr.
# If a handler is already configured, `.basicConfig` does not execute
# unless force=True.
logging.basicConfig(level=root_log_level,
    format=format, force=True)

logger = logging.getLogger(os.environ.get('APP_NAME') or 'APP')
logger.setLevel(os.environ.get('APP_LOG_LEVEL') or 'DEBUG')
