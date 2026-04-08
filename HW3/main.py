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


"""
class Clause:
    def __init__(self, clause_str):
        #clause_str is form "A B ~C"
        self.literals = set()
        for lit in clause_str.split(" "):
            if lit.startswith("~"):
                self.literals.add(-lit[1:]) #store as negative literal
            else:
                self.literals.add(lit)

    def __str__(self):
        #return string representation of clause

    def __eq__(self, other):
        #check if two clauses are equal

    def is_empty(self):
        #check if clause is empty (contradiction)

#==============Helper functions================
def are_complements(lit1, lit2):
    #return true if lit1 and lit2 are opposites
    return lit1 == -lit2

def negate_literal(lit):
    #return negation of lit

def is_tautology(clause):
    #return true if clause is a tautology

def literals_to_string(lit_set):
    #convert set of literals back to string form

#===================Resolution function=================
def resolve(clause1, clause2):
    #try to resolve two clauses. return new clause or None if can't resolve

def parse_kb_file(filename):
    #read .kb file and return (kb_clauses, goal_clause)

def main():
    #main resolution loop: read kb, resolve until goal is found or no new clauses can be generated (contradiction)


if __name__ == "__main__":


