#!/bin/bash
echo "Test easy"
time python3.4 numberlink_breadth_graph.py ../instances/easy.in > ../results_breadth_graph/log_easy.txt
echo "Test level2m"
time python3.4 numberlink_breadth_graph.py ../instances/level2m.in > ../results_breadth_graph/log_level2m.txt
echo "Test level4m"
time python3.4 numberlink_breadth_graph.py ../instances/level4m.in > ../results_breadth_graph/log_level4m.txt
echo "Test level9m"
time python3.4 numberlin_breadth_graphk.py ../instances/level9m.in > ../results_breadth_graph/log_level9m.txt
echo "Test level10m"
time python3.4 numberlink_breadth_graph.py ../instances/level10m.in > ../results_breadth_graph/log_level10m.txt
echo "Test level15m"
time python3.4 numberlink_breadth_graph.py ../instances/level15m.in > ../results_breadth_graph/log_level15m.txt
echo "Test level38s"
time python3.4 numberlink_breadth_graph.py ../instances/level38s.in > ../results_breadth_graph/log_level38s.txt
echo "Test level39s"
time python3.4 numberlink_breadth_graph.py ../instances/level39s.in > ../results_breadth_graph/log_level39s.txt
echo "Test path"
time python3.4 numberlink_breadth_graph.py ../instances/path.in > ../results_breadth_graph/log_path.txt
echo "Test wiki"
time python3.4 numberlink_breadth_graph.py ../instances/wiki.in > ../results_breadth_graph/log_wiki.txt
