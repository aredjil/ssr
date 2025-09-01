#! /bin/bash
mkdir -p ./data/raw/entropy
for n in {50..1000..50}; do
  ./build/ssr_simulator --N ${n} --m 100000 > ./data/raw/entropy/data_${n}.txt
done
echo "Done!"
