#!/bin/bash

productListFile="url_test.txt"

python3 "productList.py" > "$productListFile" 2>&1

python3 "productParameters.py" --test < "$productListFile" 2>&1

