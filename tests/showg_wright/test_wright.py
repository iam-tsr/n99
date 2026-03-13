import time
import asyncio
from wright import movies_showing
import pytest

@pytest.mark.asyncio
async def test_performance(name="inox-janak-place", code="SCJN", city="national-capital-region-ncr", date="20260314"):
    start = time.perf_counter()
    
    tasks = [movies_showing(name=name, code=code, city=city, date=date) for _ in range(5)]  # Example: 5 tasks
    await asyncio.gather(*tasks)
    end = time.perf_counter()
    print(f"Finished tasks in {end - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(test_performance()) # web scraping test using Playwright with 5 concurrent tasks which result in 3.85 seconds.