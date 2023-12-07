import pandas as pd
import matplotlib.pyplot as plt
# Primeiro, vamos definir o caminho do arquivo e tentar ler novamente
file_path = "/home/neiva/Desktop/Eng.Comp/Classes/Inteligencia_Computacional/Trabalho_Blackjack/"+"resultados.txt"

with open(file_path, 'r') as file:
    # Lendo as primeiras linhas do arquivo para análise
    first_lines = [next(file) for _ in range(5)]

first_lines


# Processando o arquivo de texto para extrair os dados necessários
data = {
    'Score': [],
    'Wins': [],
    'Loses': [],
    'Percentage': []
}

with open(file_path, 'r') as file:
    for line in file:
        if line.startswith('score:'):
            data['Score'].append(float(line.split(': ')[1].strip()))
        elif line.startswith('wins:'):
            wins = int(line.split(': ')[1].strip())
            data['Wins'].append(wins)
        elif line.startswith('loses:'):
            loses = int(line.split(': ')[1].strip())
            data['Loses'].append(loses)
            # Calculando a porcentagem de vitórias
            if wins + loses > 0:
                percentage = wins / (wins + loses) * 100
            else:
                percentage = 0
            data['Percentage'].append(percentage)

# Convertendo os dados para um DataFrame
df = pd.DataFrame(data)

# Criando o gráfico
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:red'
ax1.set_xlabel('Execução')
ax1.set_ylabel('Wins/Loses', color=color)
ax1.plot(df.index, df['Wins'], color='green', label='Wins')
ax1.plot(df.index, df['Loses'], color='red', label='Loses')
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend(loc='upper left')

ax2 = ax1.twinx()  # Criando um segundo eixo y
color = 'tab:blue'
ax2.set_ylabel('Percentage', color=color)  # Definindo o rótulo do eixo y
ax2.plot(df.index, df['Percentage'], color=color, linestyle='--', label='Percentage')
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc='upper right')

fig.tight_layout()  # Ajuste de layout
plt.title('Wins, Loses and Win Percentage over Executions')
plt.show()

