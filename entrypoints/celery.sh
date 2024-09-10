#!/bin/bash
celery --app config worker --loglevel=${WORKER_LOG_LEVEL:-INFO}
