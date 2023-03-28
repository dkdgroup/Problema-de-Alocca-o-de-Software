import pulp

# Dados de entrada
projetos = ['projeto1', 'projeto2', 'projeto3']
colaboradores = ['colab1', 'colab2', 'colab3']
skills = ['skill1', 'skill2', 'skill3']
horas_disponiveis = {
    'colab1': 30,
    'colab2': 40,
    'colab3': 35,
}
atividades = {
    ('projeto1', 'skill1'): 10,
    ('projeto1', 'skill2'): 20,
    ('projeto1', 'skill3'): 5,
    ('projeto2', 'skill1'): 15,
    ('projeto2', 'skill2'): 10,
    ('projeto2', 'skill3'): 25,
    ('projeto3', 'skill1'): 20,
    ('projeto3', 'skill2'): 10,
    ('projeto3', 'skill3'): 30,
}

competencias_colaborador = {
    ('colab1', 'skill1'): 1,
    ('colab1', 'skill2'): 1,
    ('colab1', 'skill3'): 0,
    ('colab2', 'skill1'): 0,
    ('colab2', 'skill2'): 1,
    ('colab2', 'skill3'): 1,
    ('colab3', 'skill1'): 1,
    ('colab3', 'skill2'): 0,
    ('colab3', 'skill3'): 1,
}

# Definindo o problema
prob = pulp.LpProblem("Alocacao_de_Recursos", pulp.LpMinimize)

# Variáveis de decisão
alocacao = pulp.LpVariable.dicts("alocacao",
                                  ((colab, projeto, skill) for colab in colaboradores for projeto in projetos for skill in skills),
                                  lowBound=0,
                                  cat='Integer')

# Função objetivo
prob += pulp.lpSum([alocacao[colab, projeto, skill] for colab in colaboradores for projeto in projetos for skill in skills])

# Restrições
for colab in colaboradores:
    prob += pulp.lpSum([alocacao[colab, projeto, skill] for projeto in projetos for skill in skills]) <= horas_disponiveis[colab]

for projeto, skill in atividades:
    prob += pulp.lpSum([alocacao[colab, projeto, skill] * competencias_colaborador[colab, skill] for colab in colaboradores]) >= atividades[projeto, skill]

# Resolvendo o problema
prob.solve()

# Exibindo o resultado
print("Status:", pulp.LpStatus[prob.status])

for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)