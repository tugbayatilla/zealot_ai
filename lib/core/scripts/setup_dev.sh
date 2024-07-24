dir=$(dirname "$0")
parent_dir=`dirname $dir`

python3 -m venv .venv
source $parent_dir/.venv/bin/activate

pip install --upgrade pip

which python3