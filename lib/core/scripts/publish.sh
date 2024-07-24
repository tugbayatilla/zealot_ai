dir=$(dirname "$0")
parent_dir=`dirname $dir`


# Initialize flags
test=false
prod=false
build=false

# Process command-line options
while [[ $# -gt 0 ]]
do
    case "$1" in
        -test)
            test=true
            shift
            ;;
        -prod)
            prod=true
            shift
            ;;
        -build)
            build=true
            shift
            ;;
        *)
            echo "Invalid option: $1"
            exit 1
            ;;
    esac
done


if [[ $build == true ]]; then

    echo "Build is selected as $build."
    rm -rf $parent_dir/dist

    python3 -m pip install --upgrade build
    python3 -m build $parent_dir

fi

echo "Twine will be executed."
python3 -m pip install --upgrade twine

if [[ $test == true ]]; then

    echo "Test is selected as $test."
    python3 -m twine upload --repository testpypi $parent_dir/dist/*

fi

if [[ $prod == true ]]; then

    echo "Prod is selected as $prod."
    python3 -m twine upload --repository pypi $parent_dir/dist/*

fi

