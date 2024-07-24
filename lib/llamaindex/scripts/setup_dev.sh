dir=$(dirname "$0")
parent_dir=`dirname $dir`

python3 -m venv .venv
source $parent_dir/.venv/bin/activate

pip install --upgrade pip

which python3

pip install -r ./requirements.txt --extra-index-url=https://test.pypi.org/simple/ -U