# n99
The n99 project is a movie availability tracking system built with FastAPI. It monitors movie listings on platforms like Inox and BookMyShow, allows users to register interest in specific shows, and alerts them (or updates the database) when a movie becomes available.

Architecture
The project follows a multi-layered structure, primarily located in the server/src directory.

Key Components
Backend Framework: FastAPI with Uvicorn.
Database:
PostgreSQL: Stores persistent data in user_profile, user_data, and linked_data.
Redis: Used for session management (starsessions) and temporary caching of movie selections before user profile completion.
Spiders (Crawlers):
avail_spider.py (Selenium): Scrapes currently available movies from Inox.
showg_spider.py (Playwright): Checks for specific movie availability at a cinema via BookMyShow.
Schedulers:
active_scheduler.py: Periodically checks if user-requested movies are showing using the Playwright spider.
lazy_scheduler.py: Periodically updates the global list of available movies using the Selenium spider.
File Structure & Redundancy
There is significant redundancy in the project structure:

Duplicate Packages: The directories server/config, server/model, and server/router appear to be legacy or duplicates of server/src/config, server/src/model, and server/src/router. The main.py entry point correctly uses the src package.
Module Mismatches:
src/router/api_routes.py attempts to import from src.scheduler, but the actual code resides in src/services/scheduler.
active_scheduler.py attempts to open src/scheduler/cinema-list.json, which is currently located at src/services/scheduler/cinema-list.json.
Identified Issues
WARNING

Import Errors: The project likely fails to run in its current state due to the src.scheduler import mismatch and the incorrect path for cinema-list.json.

NOTE

Database Inconsistency: init_db.py in the root directory defines a schema (users, servers) that differs from the one used by the actual application models (user_profile, user_data).

Recommendations
Refactor Directory Structure: Move services/scheduler to src/scheduler (or update imports to src.services.scheduler).
Cleanup Legacy Files: Remove the redundant server/config, server/model, and server/router directories to avoid confusion.
Consolidate Database Initialization: Update init_db.py to match the schema used by DataPG and ProfilePG.
Fix Paths: Ensure cinema-list.json is consistently referenced.
