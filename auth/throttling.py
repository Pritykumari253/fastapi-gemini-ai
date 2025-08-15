import time
from collections import defaultdict

from fastapi import HTTPException, status

# --- Constants ---
# For authenticated users
AUTH_RATE_LIMIT = 5
AUTH_TIME_WINDOW_SECONDS = 60

# For unauthenticated "global" users
GLOBAL_RATE_LIMIT = 3
GLOBAL_TIME_WINDOW_SECONDS = 60

# --- In-memory storage for user requests ---
user_requests = defaultdict(list)

# --- Throttling dependency ---
def apply_rate_limit(user_id: str):
    current_time = time.time()

    if user_id == "global_unauthenticated_user":
        rate_limit = GLOBAL_RATE_LIMIT
        time_window = GLOBAL_TIME_WINDOW_SECONDS
    else:
        rate_limit = AUTH_RATE_LIMIT
        time_window = AUTH_TIME_WINDOW_SECONDS

    # Get the current list of request times for this user
    timestamps = user_requests[user_id]

    # Calculate the cutoff time (anything older will be removed)
    cutoff_time = current_time - time_window
    recent_timestamps = []
    for t in timestamps:
        if t > cutoff_time:
            recent_timestamps.append(t)

    # Save the filtered list back for this user
    user_requests[user_id] = recent_timestamps

    if len(user_requests[user_id]) >= rate_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
        )
    else:
        # For debugging: print current usage
        current_usage = len(user_requests[user_id])
        print(f"User {user_id}: {current_usage + 1}/{rate_limit} requests used.")

    user_requests[user_id].append(current_time)
    return True