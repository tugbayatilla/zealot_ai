dir=$(dirname "$0")


# Initialize flags
test=false
prod=false
build=false
clean_dist=false
module=''

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
        -clean)
            clean_dist=true
            shift
            ;;
        -module)
            module="$2"
            shift 2
            ;;
        *)
            echo "Invalid option: $1"
            exit 1
            ;;
    esac
done

# Find valid modules by listing the folders inside the lib directory, ignoring those starting with _
valid_modules=($(find $dir/lib -mindepth 1 -maxdepth 1 -type d -not -name '_*' -exec basename {} \;))

# Validate module option
if [[ ! " ${valid_modules[@]} " =~ " ${module} " ]]; then
    echo "Invalid module: $module. Valid options are ${valid_modules[*]}."
    #exit 1
fi

module_dir=$dir/lib/$module
dist_out_dir=$dir/dist


if [[ $clean_dist == true ]]; then

    echo "clean_dist is selected as $clean_dist."
    rm -rf $dist_out_dir

fi

if [[ $build == true ]]; then

    echo "Build is selected as $build."
    python3 -m pip install --upgrade build
    python3 -m build $module_dir --outdir $dist_out_dir

fi

echo "Twine will be executed."
python3 -m pip install --upgrade twine

if [[ $test == true ]]; then

    echo "Test is selected as $test."
    python3 -m twine upload --repository testpypi $dist_out_dir/*

fi

if [[ $prod == true ]]; then

    echo "Prod is selected as $prod."
    python3 -m twine upload --repository pypi $dist_out_dir/*

fi

