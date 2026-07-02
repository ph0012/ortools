from ortools.sat.python import cp_model


model = cp_model.CpModel()

A = model.new_int_var(5, 50, "A")
B = model.new_int_var(5, 50, "B")
C = model.new_int_var(5, 50, "C")

model.add(2*A + 5*B + 3*C <= 80)
model.add(A + 2*B + 2*C <= 50)
model.maximize(25*A + 40*B + 30*C)
solver = cp_model.CpSolver()

status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print("Solution found!")
    print(solver.Value(A))
    print(solver.Value(B))
    print(solver.Value(C))

else:
    print("No solution!")