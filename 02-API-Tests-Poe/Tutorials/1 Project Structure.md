# Production Level Structure

```
Project:
|   .env
|   video_games_data.db
+---api
|   |   dependencies.py
|   |   main.py
|   |   schemas.py
|   |   __init__.py
|   +---routers
|   |   |   auth.py
|   |   |   facets.py
|   |   |   games.py
|   |   |   stats.py
+---core
|   |   config.py
|   |   security.py
|   |   __init__.py
+---database
|   |   db.py
|   |   models.py
|   |   reset.py
|   |   video_games_data.csv
|   |   __init__.py
```

## Root
| File Name     | Purpose                   |
|---------------|---------------------------|
| `.env` | Stores the environment variables. Normally, you would include this in your .gitignore but this is fake sample data  |
| `video_games_data.db` | The SQLite database that the API is using |

## API
This folder handles all the request and response logic for the API endpoints
| File Name     | Purpose                   |
|---------------|---------------------------|
| `main.py` | FastAPI app entry point that creates the app instance, includes routers, and startup configuration  |
| `dependencies.py` | Stores shared functions |
| `schemas.py` | Stores the pydantic models for request validation and response serialization |
|`__init__.py` | Makes the 'API' folder a package |

## API/routers
Instead of having to manually define url routes/endpoints in each request (which could result in a file that is hundreds of thousands of lines), you can group endpoints together using differnet files. 
| File Name     | Purpose                   |
|---------------|---------------------------|
| `auth.py` | Authentication endpoints |
| `facets.py` | Endpoints for filtering and grouping metadata (genres, platforms, publishers, etc) |
| `games.py` | Main CRUD/query endpoints for the video game records |
| `stats.py` | Aggregation endpoints (counts, trends, summaries) |

## Core
This folder stores application wide logic and configuration items
| File Name     | Purpose                   |
|---------------|---------------------------|
| `config.py` | Centralized settings |
| `security.py` | Security utilities (password hashing, JWT encoding/decoding), and helper functions |
| `__init__.py` | Makes the 'Core' folder a package |

## Database
Handles all the functionality relating to the database
| File Name     | Purpose                   |
|---------------|---------------------------|
| `db.py` | Database engine/session setup and connection manager |
| `models.py` | ORM models (tables definitions) |
| `reset.py` | A utility script to drop/recreate/reseed the database |
| `video_games_data.csv` | Seed/source dataset for initial import; used by reset.py |
| `__init__.py` | Makes the 'Core' folder a package |
