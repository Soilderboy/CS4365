"""
load_variables: reads .var file, returns dict of variable: domain
load_constraints: reads .con file, returns list of constraints (var1, var2, operator)
solve_csp: main backtracking search with heuristics and consistency
    takes variables, constraints, consistency method as input
    returns solution dict or failure


    solve csp needs:
        select unassigned variable to choose next variable to assign
        order domain to find smallest value first
        is consistent to check if current assignment is valid
        forward check to prune domains of neighbors after assignment
        record failure to log failed branches in search tree
"""

def load_variables(var_file):
    variables = {} #key = variable, value = domain list
    with open(var_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            var, domain_str = line.split(':')
            var = var.strip()
            #strip returns false for empty strings
            domain = [val.strip() for val in domain_str.split(' ') if val.strip()] #filter empty strings, then split by space, then strip each value
            variables[var] = domain #dict[var] = domain list ['1','2','3',...]
    return variables

def load_constraints(con_file):
    constraints = []
    with open(con_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split() #three parts
            var1 = parts[0].strip()
            operator = parts[1].strip()
            var2 = parts[2].strip()
            constraints.append((var1, var2, operator)) #append as tuple
    return constraints

def select_unassigned_variable(unassigned_vars, domains, constraints):
    #return variable with smallest domain, then highest constraints, then alphabetical
    min_domain_size = float('inf')
    candidates = {} #var: mcv_count
    
    for var in unassigned_vars:
        #smallest domain gets added to candidates, if tie, add to candidate,
    #inf means the first var will always be candidate, then we check
        domain_size = len(domains[var])
        if domain_size < min_domain_size:
            min_domain_size = domain_size
            candidates = {var: 0} #new candidate
        elif domain_size == min_domain_size:
            candidates[var] = 0 #tie
        #then, MCV - count how many constraints this var has with other unassigned vars
        mcv_count = 0
        for (v1, v2, op) in constraints:
            if var == v1 and v2 in unassigned_vars:
                mcv_count += 1
            elif var == v2 and v1 in unassigned_vars:
                mcv_count += 1
        
        candidates[var] = mcv_count

    #x[0] is var, x[1] is mcv_count, -x[1] for descending
    #sort will sort mcv_count first, then var name for alphabetical.
    best_var = sorted(candidates.items(), key=lambda x: (-x[1], x[0]))[0][0] #sorted gives (var, mcv_count), [0][0] gives best var
    return best_var


def order_domain_values(var, assignment, domains, constraints):
    #LCV - choose value that rules out least values in neighbors, if tie, use smaller integer
    value_constraints = {}
    #for each value in domain, count how many values it rules out in unassigned neighbor domains
    for value in domains[var]:
        ruled_out = 0
        for(v1, v2, op) in constraints:
            if var == v1 and v2 not in assignment: 
                for val in domains[v2]:
                    if not check_constraint(value, val, op):
                        ruled_out += 1
            elif var == v2 and v1 not in assignment:
                for val in domains[v1]:
                    if not check_constraint(val, value, op):
                        ruled_out += 1
        value_constraints[value] = ruled_out
    #x[1] is ruled_out count, x[0] is value, return sorted list of values by least ruled out, then smallest integer
    return [v for v, _ in sorted(value_constraints.items(), key=lambda x: (x[1], int(x[0])))]


def is_consistent(var, value, assignment, constraints):
    #check if assigning var=value violates any constraints with already assigned variables, if so, return False
    #for each constraint (var1, var2, op): if other var is assigned, check constraint is satisfied
    for (v1, v2, op) in constraints:
        if var == v1 and v2 in assignment:
            if not check_constraint(value, assignment[v2], op):
                return False
        elif var == v2 and v1 in assignment:
            if not check_constraint(assignment[v1], value, op):
                return False
    return True

def check_constraint(val1, val2, op):
    #check if val1 op val2 is true
    #operators: =, !=, <, >, <=, >=
    if op == '=':
        return val1 == val2
    elif op == '!=':
        return val1 != val2
    elif op == '<':
        return int(val1) < int(val2)
    elif op == '>':
        return int(val1) > int(val2)
    elif op == '<=':
        return int(val1) <= int(val2)
    elif op == '>=':
        return int(val1) >= int(val2)
    return False

def forward_check(var, value, domains, constraints, assignment):
    #for each constraint: if other var is unassigned, remove values that violate constraint. if that makes domain empty, return False, otherwise True
    for (v1, v2, op) in constraints:
        if var == v1 and v2 not in assignment:
            new_domain = []
            for val in domains[v2]:
                if check_constraint(value, val, op):
                    new_domain.append(val)
            if not new_domain: #if new_domain is empty, forward check fails
                    return False
            domains[v2] = new_domain #update domain
        elif var == v2 and v1 not in assignment:
            new_domain = []
            for val in domains[v1]:
                if check_constraint(val, value, op):
                    new_domain.append(val)
            if not new_domain:
                return False
            domains[v1] = new_domain
    return True

def record_failure(assignment, history):
    #Format: "VAR1=val1, VAR2=val2, ... failure"
    #variables in order they were assigned, then append "failure" to history
    assignment_str = ', '.join(f"{v}={assignment[v]}" for v in assignment)
    history.append(f"{assignment_str} failure")

def solve_csp(variables, constraints, consistency_method):
    assignment = {}
    history = []
    domains = {var: variables[var][:] for var in variables}

    def backtrack(assignment):
        if len(assignment) == len(variables):
            assignment_str = ', '.join(f"{v}={assignment[v]}" for v in assignment)
            history.append(f"{assignment_str} solution")
            return assignment
        
        #select unassigned variable using MCV, MConV, alphabetical
        unassigned_vars = [var for var in variables if var not in assignment]
        var = select_unassigned_variable(unassigned_vars, domains, constraints)
        
        #order domain values using LCV heuristic
        values = order_domain_values(var, assignment, domains, constraints)
        
        for value in values:
            assignment[var] = value

            # record failure for tried values that violate constraints immediately
            if not is_consistent(var, value, assignment, constraints):
                record_failure(assignment, history)
                del assignment[var]
                continue

            #save current domain to restore later
            saved_domains = {v: domains[v][:] for v in variables} #for all vars, v is key, domains[v] is value list, [:] to copy list

            #forward checking mode
            if consistency_method == 'fc':
                #if forward check fails, record failure and restore domains
                if not forward_check(var, value, domains, constraints, assignment):
                    record_failure(assignment, history)
                    for v in variables:
                        domains[v] = saved_domains[v]
                    del assignment[var]
                    continue

            #backtrack recursively
            result = backtrack(assignment)
            if result is not None:
                return result

            #backtrack - restore domains and try next value
            for v in variables:
                domains[v] = saved_domains[v]
            del assignment[var]
        return None
    
    backtrack(assignment)
    return history