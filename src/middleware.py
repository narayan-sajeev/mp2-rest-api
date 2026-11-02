import logging
import time
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse

# Create logger
logger = logging.getLogger(__name__)


# Log a request and attach id to response
async def log_requests(request: Request, call_next):
    # Given code
    request_id = uuid.uuid4().hex[:8]
    request.state.request_id = request_id
    started = time.perf_counter()

    try:
        # Given code
        response = await call_next(request)

    except Exception:

        # Log error and output request_id
        # Instructions say to set exc_info to True
        logger.error(f'Error processing request_id={request_id}', exc_info=True)

        # Given code
        response = JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    # Given code
    duration_ms = (time.perf_counter() - started) * 1000

    # Round duration to 1 decimal
    rounded_duration = round(duration_ms, 1)

    # Build message containing request_id, request.method, request.url.path, response.status_code and rounded_duration
    # Message string built using sample output from guide
    message = f'request_id={request_id} {request.method} {request.url.path} status={response.status_code} duration={rounded_duration}ms'

    # If error is in 500s
    if response.status_code >= 500:
        # Log message as error
        logger.error(message)
    # If error is in 400s
    elif response.status_code >= 400:
        # Log message as warning
        logger.warning(message)
    # Otherwise
    else:
        # Log message as info
        logger.info(message)

    # Given code
    response.headers["X-Request-ID"] = request_id

    return response
