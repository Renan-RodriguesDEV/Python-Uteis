# funcao soma
def soma(a, b):
    return a + b

# fatorial funcao


def fat(num):
    fat = 1
    for i in range(num, 0, -1):
        fat *= i
    return fat

# multiplica funcao


def mult(a, b):
    return a*b

# funcao sem retorno d exibir


def exibir(funcao):
    print(funcao)

# o main junta td e printa


def main():
    exibir(soma(10, 10))
    exibir(mult(10, 10))
    exibir(fat(5))


# invocacao do main
main()
