"""
Clause class:
    - store clause as set of literals
    literals can be positive or neg ~
    
    functions needed:
        are complements
        convert clause string to literal set
        convert literal set back to string
        print clause string


Basics:
    clause -> literal v ... v literal
    literal -> ~Atom | Atom
    Atom -> True | False | P | Q | ...

    conversion rules:
        p->q = ~p v q
        ~(p v q) = ~p ^ ~q
        ~(p ^ q) = ~p v ~q

File input:
    all ors are implied by spaces, all ands are implied by \n


"""
import sys #for cmd line args

class Clause:
    def __init__(self, clause_str):
        #clause_str is form "A B ~C"
        self.literals = []
        seen = set()  #track duplicates
        for lit in clause_str.split():
            if lit and lit not in seen:
                self.literals.append(lit)
                seen.add(lit)

    def __str__(self):
        #return string representation of clause
        return " ".join(self.literals)
    def __eq__(self, other):
        #check if two clauses are equal (compare as sets)
        return set(self.literals) == set(other.literals)
    def is_empty(self):
        #check if clause is empty (contradiction)
        return len(self.literals) == 0

#==============Helper functions================
def are_complements(lit1, lit2):
    #return true if lit1 and lit2 are opposites
    if lit1.startswith("~") and lit1[1:] == lit2:
        return True
    elif lit2.startswith("~") and lit2[1:] == lit1:
        return True
    else:
        return False

def negate_literal(lit):
    #return negation of lit
    if lit.startswith("~"):
        return lit[1:]
    else:
        return "~" + lit

def is_tautology(clause):
    #return true if clause is a tautology
    for lit in clause.literals:
        if negate_literal(lit) in clause.literals:
            return True
    return False

def literals_to_string(lit_set):
    #convert set of literals back to string form
    return " ".join(lit_set)

#===================Resolution function=================
def resolve(clause1, clause2):
    #try to resolve two clauses. return new clause or None if can't resolve
    for lit1 in clause1.literals:
        for lit2 in clause2.literals:
            if are_complements(lit1, lit2):
                #create new clause with all literals except complementary pair
                #new_lits = (clause1.literals - {lit1}) | (clause2.literals - {lit2})
                new_lits_str = " ".join([l for l in clause1.literals if l != lit1]
                                        + [l for l in clause2.literals if l != lit2])
                new_clause = Clause(new_lits_str)
                if not is_tautology(new_clause):
                    return new_clause
    return None

def parse_kb_file(filename):
    #read .kb file and return (kb_clauses, goal_clause)
    kb_clauses = []
    goal_clause = None
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    if lines:
        goal_clause = Clause(lines[-1]) #last line is goal
        kb_clauses = [Clause(line) for line in lines[:-1]] #all else
    return kb_clauses, goal_clause

def main():
    #main resolution loop: read kb, resolve until goal is found or no new clauses can be generated (contradiction)

    """
    Negate goal - each negated literal becomes a separate clause
    for each caluse i
        for each previous clause jj (j < i)
            try resolve i and j
            if new clause, check
                if empty (contradiction)
                    add it, then stop and output valid
                if taut, ignore
                if redundant, ignore
                otherwise, add it to list of clauses (parent info)
    if loop finishes without finding contradiction -> output "Fail"
    Output all clauses with numbers and parents
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename>")
        return
    filename = sys.argv[1]
    kb_clauses, goal_clause = parse_kb_file(filename)

    #track clauses and parents
    clauses = []
    parents = []
    seen = set() #taking forever bc of duplicate checking

    #add initial kb clauses
    for clause in kb_clauses:
        clauses.append(clause)
        parents.append(None)
        seen.add(frozenset(clause.literals))
    
    #negate goal and add as separate clauses
    for lit in goal_clause.literals:
        negated = negate_literal(lit)
        new_clause = Clause(negated)
        clauses.append(new_clause)
        parents.append(None)
        seen.add(frozenset(new_clause.literals))
    #resolution loop
    found_contradiction = False
    i = 0
    while i < len(clauses) and not found_contradiction:
        for j in range(i):
            resolvent = resolve(clauses[i], clauses[j])
            
            if resolvent is not None:
                if resolvent.is_empty():
                    #contradiction
                    clauses.append(resolvent)
                    parents.append((i+1,j+1)) #1-indexed for output
                    found_contradiction = True
                    break

                if is_tautology(resolvent):
                    continue
            
                resolvent_key = frozenset(resolvent.literals)
                if resolvent_key in seen:
                    continue

                clauses.append(resolvent)
                parents.append((i+1,j+1))
                seen.add(resolvent_key)

        i += 1

    #output
    for idx, clause in enumerate(clauses, 1):
        if clause.is_empty():
            parent_i, parent_j = parents[idx-1]
            print(f"{idx}. Contradiction {{{parent_i}, {parent_j}}}")
        else:
            if parents[idx-1] is None:
                print(f"{idx}. {clause.__str__()} {{}}")
            else:
                parent_i, parent_j = parents[idx-1]
                print(f"{idx}. {clause.__str__()} {{{parent_i}, {parent_j}}}")
    
    #final
    if found_contradiction:
        print("Valid")
    else:
        print("Fail")


if __name__ == "__main__":
    main()
