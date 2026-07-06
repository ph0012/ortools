from ortools.sat.python import cp_model

model = cp_model.CpModel()

projects = {
    "P1": {"hours" : 30, "priority" : 100},
    "P2": {"hours" : 20, "priority": 60},
    "P3": {"hours" : 15, "priority": 40},
    "P4": {"hours" : 40, "priority": 120},
    "P5": {"hours" : 25, "priority": 80},
    "P6": {"hours" : 35, "priority": 90},
    "P7": {"hours" : 10, "priority": 30},
    "P8": {"hours" : 20, "priority": 50},    
}

employees = {
    "Ana": 40,
    "Bruno": 35,
    "Carlos": 40,
    "Daniela": 30,
    "Eduardo": 40,
    "Fernanda": 20,
    "Gabriel": 40,
    "Helena": 35,
    "Igor": 25,
    "Julia": 40,
}


#region Variáveis de Decisão
work = {}
for e in employees:
    for p in projects:
        work[(e,p)] = model.new_int_var(0,projects[p]["hours"],f"{e}_{p}")

finished = {}
for p in projects:
    finished[p] = model.new_bool_var(f"finished_{p}")

participates = {}
for e in employees:
    for p in projects:
        participates[(e,p)] = model.new_bool_var(f"part_{e}_{p}")

#endregion

#region Restrições
# Restrição 1 - Funcionário não deve ultrapassar as suas horas disponíveis
for e in employees:
    model.add(sum(work[(e, p)] for p in projects) <= employees[e])

# Restrição 2 - Verificando se um funcionário participa de um projeto ou não
for e in employees:
    for p in projects:
        model.add(work[(e,p)] <= projects[p]["hours"] * participates[(e,p)])


# Restrição 3 - Horas do projeto não deve ultrapassar o seu limite
for p in projects:
    model.add(sum(work[(e,p)] for e in employees) <= projects[p]["hours"])

# Restrição 4 - Linkando projeto concluído
for p in projects:
    total = sum(work[(e,p)] for e in employees)

    model.Add(total == projects[p]["hours"]).OnlyEnforceIf(finished[p])

    model.Add(total < projects[p]["hours"]).OnlyEnforceIf(finished[p].Not())

# Restrição 5 - Fernanda só pode trabalhar em P2, P3 e P7
allowed = ["P2","P3","P7"]
for p in projects:
    if p not in allowed:
        model.add(work[("Fernanda",p)] == 0)

# Restrição 6 - Igor não pode trabalhar em projetos de duração maiores que 30 horas
for p in projects:
    if projects[p]["hours"] > 30:
        model.add(work[("Igor",p)] == 0)

# Restrição 7 - Cada funcionário pode participar de no máximo 3 projetos
for e in employees:
    model.add(sum(participates[(e,p)] for p in projects) <= 3)

# Restrição 8 - Ana e Bruno não podem trabalhar juntos no projeto P4
model.add(participates[("Ana","P4")] + participates[("Bruno","P4")] <= 1)

# Restrição 9 - O projeto P1 deve ter no mínimo dois funcionário diferentes
model.add(sum(participates[(e,"P1")] for e in employees) >= 2)

# Função objetivo
model.Maximize(sum(projects[p]["priority"] * finished[p] for p in projects ))

#endregion

solver = cp_model.CpSolver()

status = solver.solve(model)

if status == cp_model.OPTIMAL:

    print("Prioridade:", solver.ObjectiveValue())

    for p in projects:

        if solver.Value(finished[p]):

            print(f"\n{p}")

            for e in employees:

                h = solver.Value(work[(e,p)])

                if h > 0:

                    print(f"{e}: {h} horas")