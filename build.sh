#!/bin/bash

check_python_package() {
    python3 -c "import $1" 2>/dev/null
}

required_packages=("requests" "bs4" "urllib3==1.26.6")
missing_packages=()

for package in "${required_packages[@]}"; do
    if ! check_python_package "$package"; then
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo "Installing missing Python packages: ${missing_packages[*]}"
    python3 -m pip install "${missing_packages[@]}"
fi

# Additional actions, if needed