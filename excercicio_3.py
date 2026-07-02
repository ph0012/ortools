from ortools.sat.python import cp_model

model = cp_model.CpModel()

employees = [
    "Ana",    
    "Bruno",
    "Carlos",
    "Daniela",
    "Eduardo" 
]

days = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15   
]

work = {}

for e in employees:
    for d in days:
        work[(e,d)] = model.new_bool_var(f"{e}_{d}")

print(work)
exit()

for d in days:
    model.add(sum(work[(e,d)] for e in employees) == 2)

for e in employees:
    model.add(sum(work[(e,d)] for d in days) == 6)

for e in employees:
    for i in range(len(days)):
        hoje = days[i]
        amanha = days[(i+1) % len(days)]
        model.add(work[(e,hoje)] + work[(e, amanha)] <= 1)

model.add(work[("Ana", 4)] == 0)
model.add(work[("Ana", 11)] == 0)

#model.add(work[("Bruno", "Dom")] == 1)

solver = cp_model.CpSolver()

status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print("Solution found!")
    
    for d in days:
        print(f"\n{d}")
        for e in employees:
            if solver.value(work[(e,d)]):
                print("  ",e)


elif status == cp_model.INFEASIBLE:
    print("Infeasible solution!")