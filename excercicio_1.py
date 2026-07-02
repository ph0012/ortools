from ortools.sat.python import cp_model

qtd = [2500,4000,1800,6200,3700]

price = [120,85,310,42,155]

TARGET_DIFFERENCE = -150
model = cp_model.CpModel()

LIMIT = 20

delta = []

for i in range(len(qtd)):
    d = model.new_int_var(-LIMIT, LIMIT, f"d{i}")
    delta.append(d)

model.add(sum(qtd[i] * delta[i] for i in range(len(qtd))) == TARGET_DIFFERENCE)

solver = cp_model.CpSolver()

status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print("Solution found!")
    for i in range(len(qtd)):
        change = solver.Value(delta[i])
        print(change)

else:
    print("No solution!")