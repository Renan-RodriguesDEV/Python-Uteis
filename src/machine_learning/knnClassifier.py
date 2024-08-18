# %%
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv(
    'C:\\Users\\renan\\OneDrive\\Documentos\\Python Scripts\\Machine_Learning\\exemplo2.csv')

df.head(10)

# %%
plt.figure(figsize=(15, 8))
plt.scatter(df[df.risco == 'ruim'].idade,
            df[df.risco == 'ruim'].conta_corrente)
plt.scatter(df[df.risco == 'bom'].idade, df[df.risco == 'bom'].conta_corrente)
plt.xlabel('idade')
plt.ylabel('conta corrente')
plt.legend(['ruim', 'bom'])

# %%
# Para efetuar o treinamento do classificador, guardaremos as variáveis de entrada em uma variáveis chamada X e a variável de saída em y. Para tanto, utilizaremos o comando DataFrame.drop('nome_da_coluna_excluida', axis=zero_para_linhas_um_para_colunas). Para o exemplo, eliminaremos a coluna risco das variáveis de entrada.

# Criando meu X q é constando no eixo 1 apagando 'risco'
X = df.drop('risco', axis=1)
# y recebe a coluna de risco
y = df.risco

# %%
# Para executar o treinamento do classificador, criaremos um objeto da classe KNeighborsClassifier dando o nome de knn. Nesse exemplo, criaremos um KNN com número de vizinnhos igual a 3. Para tanto, passaremos o atributo n_neighbors=3. Para executar a treinamento do classificador, utilizamos o comando fit(X, y).

# estanciando e passando os (parametros) de qtde vizinho = 5
knn = KNeighborsClassifier(n_neighbors=5)

# treinando/ajustando a ia
knn.fit(X, y)

# %%
# Uma vez treinado, o classificador pode ser utilizado para determinar se um novo cliente possui risco bom ou ruim. Para tanto, utilizamos o comando predict(). Faremos a previsão do risco para um novo cliente com 18 anos e 700 reais na conta corrente.
knn.predict([[18, 700]])

# %%


# Criaremos as variáveis X_train e y_train representando os inputs e outputs de treinamento e X_test, y_test representando os inputs e outputs de teste. Na função train_test_split() passaremos como parâmetro o conjunto completo de inputs e outputs X e y juntamente com o parâmetro test_size (tamanho do conjunto de teste), que configuraremos com o valor de 0.33 (1/3). Para fixar a aleatoriedade da divisão dos conjuntos, configuraremos o parâmetro random_state=42

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=1/3, random_state=42)

# *100 para exibir em procentagem
accuracy_score(y, knn.predict(X))*100


# %%
# Criaremos um novo classificador KNN configurado com n_neighbors=5 e o chamaremos de knn2. Uma vez treinado, calcularemos a acuracidade do classificador utilizando a função accuracy_score() que recebe como parâmetros os inputs conhecidos e os inputs previstos.

knn2 = KNeighborsClassifier(n_neighbors=5)
knn2.fit(X_treino, y_treino)

accuracy_score(y_teste, knn2.predict(X_teste))*100

# %%
# Podemos aumentar a qualidade do classificador através do tratamento dos inputs. Para classificadores baseados em cálculo de distância, obetemos resultados melhores através da normalização das variáveis de input. Nesse caso, temos duas variáveis que possuem escalas distintas (idade e conta corrente). Aplicando uma função de normalização, podemos aumentar significamente a qualidade da acurácia.

# Para o exemplo, aplicaremos o normalizador MinMaxScaler, comprimindo os dados no intervalo entre 0 e 1. Criaremos um objeto da classe MinMaxScaler chamado normalizador e utilizaremos o comando MinMaxScaler.fit_transform() para ajustar o normalizador aos dados e executar a transformação do mesmo, passando como parâmetro os inputs X.


normalizador = MinMaxScaler()
X_norm = normalizador.fit_transform(X)
X_norm

# %%
# Para verificar se houve melhoria na qualidade do classificador, repetimos o procedimento de teste.

X_train, X_test, y_train, y_test = train_test_split(
    X_norm, y, test_size=0.33, random_state=42)

knn3 = KNeighborsClassifier(n_neighbors=5)
knn3.fit(X_train, y_train)

accuracy_score(y_test, knn3.predict(X_test))

# %%

# Para dados normalizados, precisamos aplicar a mesma normalização executada nos dados de treinamento, nos dados de previsão utilizando o comando MinMaxScaler.transform(). Para prever o risco de um novo cliente com 18 anos e movimentação de 1000 reais, por exemplo, não podemos passar esses valores sem aplicar a normalização.

X_new = [[18, 1000]]
X_new = normalizador.transform(X_new)
knn3.predict(X_new)
