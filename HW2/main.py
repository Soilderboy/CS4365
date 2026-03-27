"""
Main: 
CSP solver with three args: path to .var, path to .con, and consistency method(none, fc)
Output: search tree branches visited during solving

.var = variables and domains
.con = binary constraints using operators

Search with heuristics:
    MCV -> smallest domain first, then highest constraints
    MConV -> alphabetical tie breaker
    Value selection: LCV -> smallest value tie break

Modes:
    none - pure backtracking
    fc - forward checking, arc consistency check after each assignment

output format:
    VAR1=val1, VAR2=val2, ... (solution|failure)

Python 3.8.18 with main.py as entry point.
Run on Linux 22.04, 10 min timeout, 3gb ram max

No non-standard libraries except numpy and pandas
"""

import sys
import cspsolver #contains load_variables, load_constraints, solve_csp

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <path_to_var_file> <path_to_con_file> <consistency_method>")
        sys.exit(1)
    var_file = sys.argv[1]
    con_file = sys.argv[2]
    consistency_method = sys.argv[3]
    #load variables and constraints
    variables = cspsolver.load_variables(var_file)
    constraints = cspsolver.load_constraints(con_file)

    #solve csp
    print("Search tree branches:")
    history = cspsolver.solve_csp(variables, constraints, consistency_method)
    #if history is not empty, print search tree branches
    for i, branch in enumerate(history, 1): #enumerate returns (index, value) starting from 1
        print(f"Branch {i}: {branch}")

if __name__ == "__main__":
    main()



