#!/bin/bash
echo "Test easy"
python3.4 numberlink.py ../instances/easy.in > ../results/log_easy.txt
echo "Test level2m"
python3.4 numberlink.py ../instances/level2m.in > ../results/log_level2m.txt
echo "Test level4m"
python3.4 numberlink.py ../instances/level4m.in > ../results/log_level4m.txt
echo "Test level9m"
python3.4 numberlink.py ../instances/level9m.in > ../results/log_level9m.txt
echo "Test level10m"
python3.4 numberlink.py ../instances/level10m.in > ../results/log_level10m.txt
echo "Test level15m"
python3.4 numberlink.py ../instances/level15m.in > ../results/log_level15m.txt
echo "Test level38s"
python3.4 numberlink.py ../instances/level38s.in > ../results/log_level38s.txt
echo "Test level39s"
python3.4 numberlink.py ../instances/level39s.in > ../results/log_level39s.txt
echo "Test path"
python3.4 numberlink.py ../instances/path.in > ../results/log_path.txt
echo "Test wiki"
python3.4 numberlink.py ../instances/wiki.in > ../results/log_wiki.txt
