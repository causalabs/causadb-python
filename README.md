# CausaDB

An easy-to-use platform for building and querying causal AI models in the cloud.

## Developers

This project uses the Poetry package manager. To get it set up, run

```
poetry install
```

### CLI

You can test out the CLI by running

```
poetry run causadb <command_here>
```

The Typer documentation has a great article on using Typer with Poetry: https://typer.tiangolo.com/tutorial/package.

### Local development

When running in local development mode, there'll be a local CausaDB instance running, likely on port 8000. The client will automatically point towards the production URL, but this can be overridden for local development by setting `CAUSADB_API_URL` in the `.env` file. Use the `.env.template` file as a template for this. The API URL should be set to `http://localhost:8000` when running in local development mode. It is designed this way so that when running in production, the environment variable will be missing and will fall back to the production API URL.