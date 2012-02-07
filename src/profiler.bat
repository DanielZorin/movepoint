python.exe -m cProfile -s time Profile.py > prof2-time.txt

python.exe -m cProfile -s cumulative Profile.py > prof2-cumtime.txt
