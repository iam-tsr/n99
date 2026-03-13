import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from server.model.core.showg_spider import movies_showing
import resource
import time

movies_showing(name="inox-janak-place", code="SCJN", city="national-capital-region-ncr", date="20260303")

# Get resource usage statistics for the current process
usage = resource.getrusage(resource.RUSAGE_SELF)

print(f"User time used: {usage.ru_utime} seconds")
print(f"System time used: {usage.ru_stime} seconds")
# Note: ru_maxrss unit varies by OS (often kilobytes on Linux)
print(f"Peak Memory Usage (ru_maxrss): {usage.ru_maxrss} (units depend on OS)")
