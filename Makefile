run:
\tpython3 experiments/run_all.py

up:
\tdocker compose up --build

verify:
\tpython3 -c "import json; d=json.load(open('benchmarks/summary.json')); assert d['all_pass'], d; print('ALL GREEN')"

clean:
\trm -rf benchmarks/exp*.json benchmarks/summary.json __pycache__ experiments/__pycache__
