from fastapi import Request, HTTPException
from ipaddress import ip_address
from typing import Dict

request_counts: Dict[str, int] = {}

# set up rate limiter
RATE_LIMIT = 10  # number of requests allowed per IP address
RATE_LIMIT_DURATION = 3600  # time frame for rate limit (in seconds)

@app.middleware("http")
def rate_limiter(request: Request, call_next):
    # get IP address from request
    ip = ip_address(request.client.host)

    # check if IP address has exceeded limit
    if str(ip) in request_counts and request_counts[str(ip)] >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")

    # increment request count for IP address
    if str(ip) not in request_counts:
        request_counts[str(ip)] = 1
    else:
        request_counts[str(ip)] += 1

    response = call_next(request)

    return response
