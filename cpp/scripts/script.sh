#!/bin/bash

for N in $(seq 200 200 800);
do 
    for mu in $(seq 1.5 0.1 3.0);
    do
        ./main.x --mu ${mu} --n ${N} > ./data/durations/data_${N}_${mu}.txt
    done 
done 
echo "Done!"