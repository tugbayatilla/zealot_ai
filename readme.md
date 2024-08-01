## How to use publish
```
 . ./publish.sh -build -module ally -clean -test -prod 
```
-build: builds
-module: mandatory 
-clean: removes dist folder
-test: published to testpypi
-prod: publishes to pypi

## Setup Dev Environment

```sh
. ./setup_dev.sh
```
### Set Environment Variables

- LLM__API_KEY=
- EMBEDDINGS__API_KEY=

> Important: after creating .env file, vscode might not execute tests correctly. Close vscode and open again. :)

## Run Tests

```sh
pytest -v -m "not integration"
```

## Run Coverage

```sh
coverage run -m pytest -v && coverage report -m
```