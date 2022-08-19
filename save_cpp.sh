#! /bin/bash
# compile specified file into prog and execute immediately
# ex. in root "./save_cpp.sh 18Aug22/app"

clear
clang++ -std=c++17 $1.cpp -o prog
./prog