#!/bin/bash
echo "Test easy"
time python3.4 numberlink.py ../instances_breadth_tree/easy.in > ../results_breadth_tree/log_easy.txt
echo "Test level2m"
time python3.4 numberlink_breadth_tree.py ../instances/level2m.in > ../results_breadth_tree/log_level2m.txt
echo "Test level4m"
time python3.4 numberlink_breadth_tree.py ../instances/level4m.in > ../results_breadth_tree/log_level4m.txt
echo "Test level9m"
time python3.4 numberlink_breadth_tree.py ../instances/level9m.in > ../results_breadth_tree/log_level9m.txt
echo "Test level10m"
time python3.4 numberlink_breadth_tree.py ../instances/level10m.in > ../results_breadth_tree/log_level10m.txt
echo "Test level15m"
time python3.4 numberlink_breadth_tree.py ../instances/level15m.in > ../results_breadth_tree/log_level15m.txt
echo "Test level38s"
time python3.4 numberlink_breadth_tree.py ../instances/level38s.in > ../results_breadth_tree/log_level38s.txt
echo "Test level39s"
time python3.4 numberlink_breadth_tree.py ../instances/level39s.in > ../results_breadth_tree/log_level39s.txt
echo "Test path"
time python3.4 numberlink_breadth_tree.py ../instances/path.in > ../results_breadth_tree/log_path.txt
echo "Test wiki"
time python3.4 numberlink_breadth_tree.py ../instances/wiki.in > ../results_breadth_tree/log_wiki.txt
