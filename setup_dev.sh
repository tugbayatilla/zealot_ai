python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip

which python3

pip install -r ./requirements.txt

#copy this path to .env for vscode
cat > .env << EOL
PYTHONPATH=./lib/core:./lib/langchain:./lib/llamaindex:./lib/ally:./lib/chroma:./lib/langsmith
LLM__API_KEY=
EMBEDDINGS__API_KEY=
EOL