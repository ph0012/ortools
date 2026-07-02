from ortools.sat.python import cp_model

# Quantities
qty = [
    2400,
    30000,
    13982,
    118400,
    2000,
    89717,
    123200,
    43200,
    18639,
    33400,
    220700,
    29300,
    3650,
    8400,
    28636,
    37400,
    243472,
    4000,
    6500,
    4950,
    4950,
    59500,
    3800,
    7280,
    48860,
    48860,
    42074,
    271820,
    4523,
    48860
]

# Current unit prices
price = [

    31640,
140,
609,
40254,
8767,
407,
1721,
1544,
1167,
1301,
718,
853,
4160,
55284,
12086,
9889,
1125,
44758,
46930,
30953,
2176,
1816,
8878,
92407,
11439,
741,
951,
2487,
54997,
5309
]

TARGET_DIFFERENCE = -561

model = cp_model.CpModel()

# Maximum adjustment allowed in each unit price
LIMIT = 20

delta = []

for i in range(len(qty)):
    d = model.NewIntVar(-LIMIT, LIMIT, f"d{i}")
    delta.append(d)

# Exact total adjustment
model.Add(
    sum(qty[i] * delta[i] for i in range(len(qty)))
    == TARGET_DIFFERENCE
)

# Auxiliary variables for |delta|
abs_delta = []

for i, d in enumerate(delta):
    a = model.NewIntVar(0, LIMIT, f"abs{i}")
    model.AddAbsEquality(a, d)
    abs_delta.append(a)

# Objective:
# minimize total change in unit prices
model.Minimize(sum(abs_delta))

solver = cp_model.CpSolver()

status = solver.Solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):

    print("Solution found!\n")

    total = 0

    for i in range(len(qty)):
        change = solver.Value(delta[i])

        if change != 0:

            impact = change * qty[i]
            total += impact

            print(
                f"Row {i+1}: "
                f"Quantity={qty[i]}, "
                f"Price {price[i]} -> {price[i]+change}, "
                f"Change={change:+d}, "
                f"Impact={impact:+d}"
            )

    print("\nTotal impact:", total)

else:
    print("No solution.")