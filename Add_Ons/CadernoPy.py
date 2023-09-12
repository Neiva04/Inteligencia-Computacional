print('Digite seu nome')
name = input()
print('hello %s' % name)
# pra printar variavel

print ('Quantos anos vc tem?')
age = int(input())
condicional = input('ja fez aniversario?')
if condicional == 'sim':
    print('{0}, {1}'.format(name, age))
#dois vairavel pra printar ( . FORMAT ( , ) )
# Ou ( print( f ' { } ' ) )

ages = 2022 - int(age)
#transformando input() (sring) em int

print(f'\n{name}, {ages}')

altura = float(input('agora sua altura?'))
#trasformar 3 linhas (print, input e transformação) em 1

print(f'sua altura eh:{altura}')

for name in range(0, 9):
    print(name)
    