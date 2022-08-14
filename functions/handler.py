#!/usr/local/bin/python

"""
An example function that shows how to use proc_wrapper's embedded mode.
"""

from typing import Any, Mapping

import datetime
import os

from proc_wrapper import ProcWrapper, ProcWrapperParams

from .logger import logger

LOCAL_DEVELOPMENT_RUN_ENVIRONMENT_NAME = 'localdev'


def make_result(value: str) -> str:
    """ A simple testable function that concatenates a string. """
    return value + ' -- SUCCESS!'


def _run_internal(wrapper: ProcWrapper, cbdata: str,
        config: Mapping[str, Any]) -> str:
    logger.debug(f"{config=}")

    result = make_result(cbdata)
    wrapper.update_status(success_count=1, last_status_message=result)
    return result


def make_proc_wrapper_params(task_name: str) -> ProcWrapperParams:
    """ Create a configured instance of proc_wrapper_params. """
    proc_wrapper_params = ProcWrapperParams()

    deployment = os.getenv('DEPLOYMENT', LOCAL_DEVELOPMENT_RUN_ENVIRONMENT_NAME)
    proc_wrapper_params.deployment = deployment

    # For local development, read a local file, which should be filled in from
    # config.localdev.json.sample and copied to config.localdev.json
    #
    # When running with AWS Lambda, proc_wrapper will get its configuration
    # locations from the environment variable PROC_WRAPPER_CONFIG_LOCATIONS
    # which is set by serverless.yml
    if deployment == LOCAL_DEVELOPMENT_RUN_ENVIRONMENT_NAME:
        proc_wrapper_params.config_locations = [
            "file://config.localdev.json",
        ]

    app_name = os.environ.get('APP_NAME', 'app')

    proc_wrapper_params.auto_create_task = True
    proc_wrapper_params.task_is_passive = False
    proc_wrapper_params.schedule = os.environ.get('EXECUTION_SCHEDULE', '')
    proc_wrapper_params.task_name = app_name + '_' + task_name + '_' + deployment
    proc_wrapper_params.auto_create_task_run_environment_name = os.environ.get(
        'PROC_WRAPPER_AUTO_CREATE_TASK_RUN_ENVIRONMENT_NAME', deployment)
    proc_wrapper_params.auto_create_task_props = {
        'project_url': os.environ.get('PROJECT_URL', '')
    }

    return proc_wrapper_params

def run(task_name: str, event: Any, context: Any) -> str:
    """
    Helper function that configures proc_wrapper before running the
    main code.
    """
    logger.info(f"Received {event=}")

    proc_wrapper_params = make_proc_wrapper_params(task_name=task_name)
    wrapper = ProcWrapper(params=proc_wrapper_params,
        runtime_context=context, input_value=event)

    result = wrapper.managed_call(_run_internal, data=task_name)

    current_time = datetime.datetime.now().time()
    logger.info("Your function %s ran at %s", task_name, current_time)
    logger.info(f"{result=}")

    return result


def run_rate(event: Any, context: Any) -> str:
    """ Entrypoint from AWS Lambda, for the function run at a fixed rate. """
    return run(task_name="rate", event=event, context=context)


def run_cron(event: Any, context: Any) -> str:
    """ Entrypoint from AWS Lambda, for the function run on a cron schedule. """
    return run(task_name="cron", event=event, context=context)


if __name__ == "__main__":
    run(task_name='local', event=None, context=None)
