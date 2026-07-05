from ortools.sat.python import cp_model

model = cp_model.CpModel()

projects = [
    ("P1",30,100),
    ("P2",20,60),
    ("P3",15,40),
    ("P4",40,120),
    ("P5",25,80),
    ("P6",35,90),
    ("P7",10,30),
    ("P8",20,50),    
]

employees = [
    ("Ana", 40),
    ("Bruno",35),
    ("Carlos",40),
    ("Daniela",30),
    ("Eduardo",40),
    ("Fernanda",20),
    ("Gabriel",40),
    ("Helena",35),
    ("Igor",25),
    ("Julia",40),
]


work = {}

for e, ch in employees:
    for pro, h, pri in projects:
        work[(e,pro)] = model.new_int_var(0,h,f"{e}_{pro}")

for e, ch in employees:
    model.add(sum(work[(e,pro)] for pro, h, pri in projects) <= ch)

for pro,h,pri in projects:
    model.add(sum(work[(e,pro)] for e, ch in employees) == h)

#model.maximize(sum(work[("Ana",projects[i][0])] for i in range(len(projects))))

solver = cp_model.CpSolver()

status = solver.solve(model)

if status == cp_model.OPTIMAL:
    for p in projects:
        print("\n",p[0])
        for e in employees:
            horas = solver.value(work[(e[0],p[0])])
            print("   ",f"{e[0]} -> {horas}")
        
        
    print(solver.ObjectiveValue())
else:
    print("No solution!")
exit()


finish = {}

for p, h, priority in projects:
    finish[p] = model.new_bool_var(p)

model.add(finish["P1"] == (projects[0][1] == 30))

#print(projects[0][1] == 30)
#exit()

print(sum(priority * finish[p] for p, h, priority in projects))

model.maximize(sum(priority * finish[p] for p, h, priority in projects))

solver = cp_model.CpSolver()

status = solver.solve(model)

if status == cp_model.OPTIMAL:
    print(solver.ObjectiveValue())