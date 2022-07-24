#!/usr/bin/env bash

set -e

if [[ -z $1 ]]
  then
    if [[ -z $DEPLOYMENT_ENVIRONMENT ]]
      then
        echo "Usage: $0 <deployment> [task_names]"
        exit 1
    fi
  else
    DEPLOYMENT_ENVIRONMENT=$1
fi

if [[ -z $NVM_DIR ]]
  then
    NVM_DIR="~/.nvm"
fi

. $NVM_DIR/nvm.sh

nvm install
nvm exec npm install
pyenv install --skip-existing
export APP_TASK_VERSION_SIGNATURE=`git rev-parse HEAD`
nvm exec npm run sls -- deploy --stage=$DEPLOYMENT_ENVIRONMENT
