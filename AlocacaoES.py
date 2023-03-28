#trazendo dados do cplex ibm
from docplex.mp.model import Model
import pandas as pd
import cplex


# Dados do problema referentes a alguns dados estraidos da mobly
projetos = ['Bob', 'Alice']
colaboradores = ['Alvanir', 'Shigueru', 'Laino']
habilidades = ['java', 'php', 'mysql', 'vue.js', 'angular', 'laravel', 'python', 'devops', 'github', 'phalcon', 'teste']

# Crie um DataFrame com as habilidades dos colaboradores
habilidades_colab = pd.DataFrame([
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
], columns=habilidades, index=colaboradores)

#Horas de cada membro da equipe
horas_trabalhadas = {'Alvanir': 40, 'Shigueru': 40, 'Laino': 40}

#requisitos necessários para cada projeto
atividades = {
            'Bob':
                {'php': 40, 'zend': 20, 'mysql': 20, 'phalcon': 10, 'teste': 5, 'github': 10},
            'Alice':
                {'php': 30, 'mysql': 20, 'angular': 40, 'laravel': 20, 'devops': 10}
            }

# Crie um modelo de otimização
mdl = Model("Alocação de Recursos")

# Variáveis de decisão
x = mdl.binary_var_matrix(colaboradores, projetos, name=lambda ns: "x_%s_%s" % ns)

# Função objetivo: minimizar o número total de colaboradores alocados
mdl.minimize(mdl.sum(x))

# Restrições: horas trabalhadas e habilidades
for projeto, requisitos in atividades.items():
    for habilidade, horas in requisitos.items():
        mdl.add_constraint(
            mdl.sum(habilidades_colab.loc[colab, habilidade] * x[colab, projeto] for colab in colaboradores) >= horas,
            ctname="requisito_%s_%s" % (projeto, habilidade))

for colab, horas_disp in horas_trabalhadas.items():
    mdl.add_constraint(
        mdl.sum(x[colab, projeto] for projeto in projetos) <= horas_disp / 40,
        ctname="horas_%s" % colab)

# Resolva o modelo usando solver
solucao = mdl.solve()

#validando chamada do solver
print(mdl.solve())

# Exiba a solução
if solucao:
    print("Solução encontrada:")
    for colab in colaboradores:
        for projeto in projetos:
            if x[colab, projeto].solution_value > 0:
                print("Colaborador %s alocado para %s" % (colab, projeto))
else:
    print("Nenhuma solução encontrada.")