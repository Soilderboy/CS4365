# Resolution Theorem Prover - Implementation Guide

## Input Format (task7.in example)

```
~NoLeakH1 ~NoLeakH2 NoLeak ~LowTemp ReactorUnitSafe V1 V2 okH1 okH2 l    [Clause 1 - KB]
~NoLeak ~LowTemp ReactorUnitSafe                                         [Clause 2 - KB]
~NoLeakH1 ~NoLeakH2 NoLeak                                               [Clause 3 - KB]
~okH1 NoLeakH1                                                           [Clause 4 - KB]
okH1 V1 NoLeakH1                                                         [Clause 5 - KB]
~okH2 NoLeakH2                                                           [Clause 6 - KB]
okH2 V2 NoLeakH2                                                         [Clause 7 - KB]
~l ~V1 ~V2 LowTemp                                                       [Clause 8 - KB]
l ~V1 LowTemp                                                            [Clause 9 - KB]
l ~V2 LowTemp                                                            [Clause 10 - KB]
~l                                                                        [Clause 11 - WHAT TO PROVE]
```

**Key Points:**
- Each line is a clause (disjunction of literals)
- Literals are space-separated
- Negation is marked with `~` prefix
- **Last clause is what we need to prove**
- Everything before is the KB

## Algorithm Flow

1. **Parse KB** - read all clauses into a list
2. **Negate the goal** - take the last clause and negate it
   - Goal: `~l` 
   - Negate: `l`
   - Add to KB
3. **Apply Resolution** - loop through clauses:
   - For each clause `i`, try to resolve with all previous clauses `j` (where `j < i`)
   - If two clauses share a complement pair, resolve them
   - Add new clause to KB (if not redundant/tautology)
4. **Detect Success/Failure**:
   - If `False` (empty clause) is generated → **Valid**
   - If no more resolutions possible → **Fail**
5. **Output** - print all clauses with parents

## What "Complement" Means

- `p` and `~p` are complements
- If Clause A has `p` and Clause B has `~p`, they can resolve
- Resolution removes both, combines the rest

## What "Redundant" Means

- Clause A is redundant if another clause is identical (same literals)
- Example: `p q r` is redundant if `p q r` already exists

## What "Tautology" Means

- A clause that contains both a literal and its negation is always true
- Example: `p ~p q` is a tautology (never needs to be stored)
- Don't add tautologies to KB

## Output Format

```
1. ~NoLeakH1 ~NoLeakH2 NoLeak ~LowTemp ReactorUnitSafe V1 V2 okH1 okH2 l {}
2. ~NoLeak ~LowTemp ReactorUnitSafe {}
...
11. l {}
12. <new clause from resolution> {i, j}
...
Final: Valid or Fail
```
