from ortools.sat.python import cp_model

model = cp_model.CpModel()

employees = [
    "Ana",
    "Bruno",
    "Carlos",
    "Daniela",
    "Eduardo",
    "Fernanda",
    "Gabriela",    
]

days = [
    "Seg",
    "Ter",
    "Qua",
    "Qui",
    "Sex",
    "Sab",
    "Dom",    
]

work = {}

for e in employees:
    for d in days:
        work[(e,d)] = model.new_bool_var(f"{e}_{d}")

for d in days:
    model.add(sum(work[(e,d)] for e in employees) == 2)

for e in employees:
    model.add(sum(work[(e,d)] for d in days) == 2)

for e in employees:
    for i in range(len(days)):
        hoje = days[i]
        amanha = days[(i+1) % len(days)]
        model.add(work[(e,hoje)] + work[(e,amanha)] <=1) 

model.add(work[("Ana","Sex")] == 0)
model.add(work[("Bruno","Dom")] == 1)

solver = cp_model.CpSolver()

status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print("Solution found!")
    for d in days:
        print(d)
        for e in employees:
            if solver.value(work[(e,d)]):
                print("   ",e)

else:
    print("No solution!")