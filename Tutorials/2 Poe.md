# What is Poe?

PoeThePoet (Poe) is a task runner that works in conjunction with uv or poetry. It provides a simple way to define project tasks within your pyproject.toml, and either a standalone CLI or a poetry plugin to run them using your project’s virtual environment.

## Installation
```
uv add poethepoet --dev
```

## Usage
In your `pyproject.toml` file, you can add the `[tool.poe.tasks]` header and place commonly use commands underneath.
```
[tool.poe.tasks] 
api_dev = "uv run fastapi dev api/main.py"
reset_database = "uv run database/reset.py"
chain = ["api_dev", "reset_database"]
```

In the above reference, the api_dev command will execute "fastapi dev api/main.py" in the command line.

To actually execute the commands, you can run the following in your command terminal:
```
uv run poe api_dev
```

