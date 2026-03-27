.PHONY: test1 test2 test3 clean

test1:
	@echo "=== Test 1: ex1.var + ex1.con (none) ==="
	python main.py ex1.var ex1.con none
	@echo "\n=== Test 1: ex1.var + ex1.con (fc) ==="
	python main.py ex1.var ex1.con fc

test2:
	@echo "=== Test 2: ex2.var + ex2.con (none) ==="
	python main.py ex2.var ex2.con none
	@echo "\n=== Test 2: ex2.var + ex2.con (fc) ==="
	python main.py ex2.var ex2.con fc

test3:
	@echo "=== Test 3: ex3.var + ex3.con (none) ==="
	python main.py ex3.var ex3.con none
	@echo "\n=== Test 3: ex3.var + ex3.con (fc) ==="
	python main.py ex3.var ex3.con fc

clean:
	rm -f *.pyc __pycache__
