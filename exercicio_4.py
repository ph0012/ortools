from ortools.sat.python import cp_model

model = cp_model.CpModel()

items = [
    ("Notebook",4,4500),
    ("Drone",6,5200),
    ("Camera",3,3500),
    ("Bateria",2,1800),
    ("GPS",5,2500),
    ("Barraca",15,4200),
    ("Comida",8,1600),
    ("Agua",10,1200),
    ("Casaco",6,1500),
    ("KitMedico",5,2800),    
]

take = {}

for name, weight, value in items:
    take[name] = model.new_bool_var(name)

model.add(sum(weight * take[name] for name,weight, value in items) <= 40)

model.add(take["Drone"] + take["Notebook"] <= 1)

model.add(take["Barraca"] <= take["Agua"])

model.add(take["Drone"] <= take["Bateria"])

model.maximize(sum(value * take[name] for name, weight, value in items))

solver = cp_model.CpSolver()

status = solver.solve(model)

if status == cp_model.OPTIMAL:
    print("Solution found!")
    for name, weight, value in items:
        
        if solver.value(take[name]):
            print(name)
        else:
            print(f"{name} - não levar")

else:
    print("No solution!")