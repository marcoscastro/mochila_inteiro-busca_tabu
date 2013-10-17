# -*- coding:utf-8 -*-
# Autor: Marcos Castro
# Busca Tabu - Problema da Mochila Inteiro

# Configuração da Mochila
# Objeto	(j)		1	2	3	4	5
# Peso		(wj)		4	5	7	9	6
# Benefício	(pj)		2	2	3	4	4

# Objetivo: Maximizar o benefício de cada elemento
# Função objetivo: f(s) = SOMATORIO[j=1 até n](pj)(sj) - SOMATORIO[j=1 até n](pj)(sj) * max{0, SOMATORIO[j=1 até n](wj)(sj) - b}
# Função objetivo resumida: f(s) = SOMATORIO[j=1 até n](pj)(sj) * [1 - max{0, SOMATORIO[j=1 até n](wj)(sj) - b}]
# Função de vizinhança: alterar apenas um dos bits (como os vizinhos vão ser gerados)

# função para obter o peso de determinada solução
# essa função calcula o somatório do peso
# passa uma solução e a mochila
def obter_peso(solucao, mochila):
	peso = 0
	for i in range(0, len(solucao)):
		peso += solucao[i] * mochila[i][0]
	return peso

# função que calcula o valor da função objetivo
# passa uma solução, a mochila e a capacidade máxima da mochila
def obter_avaliacao(solucao, mochila, capacidade_maxima):
	somatorio_peso = 0
	somatorio_beneficio = 0
	for i in range(0, len(solucao)):
		somatorio_peso += solucao[i] * mochila[i][0] # mochila[i][0] acessa o peso
		somatorio_beneficio += solucao[i] * mochila[i][1] # mochila[i][1] acessa o benefício
	avaliacao = somatorio_beneficio * (1 - max(0, somatorio_peso - capacidade_maxima))
	return avaliacao

# função para gerar os vizinhos, a vizinhança é gerada trocando o bit
# melhor_solucao - melhor solução corrente
# max_vizinhos - quantidade máxima de vizinhos
def gerar_vizinhos(melhor_solucao, max_vizinhos):
	vizinhos = []
	pos = 0
	for i in range(0, max_vizinhos):
		vizinho = []
		for j in range(0, len(melhor_solucao)):
			if  j == pos:
				if melhor_solucao[j] == 0:
					vizinho.append(1)
				else:
					vizinho.append(0)
			else:
				vizinho.append(melhor_solucao[j])
		vizinhos.append(vizinho)
		pos += 1
	return vizinhos

# função para obter o valor de avaliação de cada vizinho
# vizinhos - lista de todos os vizinhos
# mochila - a mochila
# capacidade_maxima - capacidade máxima da mochila
# max_vizinhos - quantidade máxima de vizinhos
def obter_avaliacao_vizinhos(vizinhos, mochila, capacidade_maxima, max_vizinhos):
	vizinhos_avaliacao = []
	for i in range(0, max_vizinhos):
		vizinhos_avaliacao.append(obter_avaliacao(vizinhos[i], mochila, capacidade_maxima))
	return vizinhos_avaliacao

# função para obter o bit modificado
# melhor_solucao - melhor solução corrente
# melhor_vizinho - melhor vizinho
def obter_bit_modificado(melhor_solucao, melhor_vizinho):
	for i in range(0, len(melhor_solucao)):
		if melhor_solucao[i] != melhor_vizinho[i]:
			return i

# função para obter o vizinho com a máxima avaliação
# vizinhos_avaliacao - valor de avaliação de todos os vizinhos
# lista_tabu - lista tabu para proibir determinada modificação de bit
# melhor_solucao - melhor solução corrente
# vizinhos - lista com todos os vizinhos
def obter_vizinho_melhor_avaliacao(vizinhos_avaliacao, lista_tabu, melhor_solucao, vizinhos):
	maxima_avaliacao = max(vizinhos_avaliacao)
	pos = 0
	bit_proibido = -1
	# verifica se a lista tabu não possui elementos
	if len(lista_tabu) != 0:
		# se possuir, é porque tem bit proibido, então pega esse bit
		bit_proibido = lista_tabu[0]
	# for para obter a posição do melhor vizinho
	for i in range(0, len(vizinhos_avaliacao)):
		if vizinhos_avaliacao[i] == maxima_avaliacao:
			pos = i
			break
	# verifico se o vizinho é resultado de movimento proibido
	if bit_proibido != -1:
		# se for, então obtém a posição do bit que foi modificado para gerar esse vizinho
		bit_pos = obter_bit_modificado(melhor_solucao, vizinhos[pos])
		# verifica se é um bit que está na lista_tabu (compara com bit_proibido)
		if bit_pos == bit_proibido:
			# se cair nesse if, então procura o segundo melhor vizinho
			melhor_pos = 0
			for i in range(1, len(vizinhos_avaliacao)):
				if i != bit_pos:
					if vizinhos_avaliacao[i] > vizinhos_avaliacao[melhor_pos]:
						melhor_pos = i
			return melhor_pos # retorna a posição do segundo melhor vizinho
	return pos # retorna a posição do melhor vizinho

# configuração da mochila com uma lista de listas
# o primeiro é o peso e o segundo é o benefício
mochila = [[4,2], [5,2], [7,3], [9,4], [6,4]]
iteracao = melhor_iteracao = 0
melhor_solucao = [] # irá guardar a melhor solução
lista_tabu = [] # lista tabu inicialmente vazia
capacidade_maxima = 23 # capacidade máxima da mochila
bt_max = 1 # quantidade máxima de iterações sem melhora no valor da melhor solução
max_vizinhos = 5 # quantidade máxima de vizinhos

# PASSO 0
# gera uma solução inicial aleatória
import random # módulo para gerar números randômicos
# o for abaixo gera 5 vezes os números: 0 ou 1
for i in range(0, 5): 
	bit = random.randrange(2) # gera números de 0 (inclusive) a 1 (inclusive)
	melhor_solucao.append(bit) # adiciona o bit na lista

# mostra a solução inicial e o seu valor de avaliação
print('Solução inicial: {0}, Avaliação: {1}'.format(melhor_solucao, obter_avaliacao(melhor_solucao, mochila, capacidade_maxima)))

# obtém o peso corrente da mochila
peso_corrente = obter_peso(melhor_solucao, mochila)
# obtém a avaliação da melhor_solucao
melhor_avaliacao = obter_avaliacao(melhor_solucao, mochila, capacidade_maxima)

# gera os vizinhos (vizinhança)
vizinhos = gerar_vizinhos(melhor_solucao, max_vizinhos)
# calcula a avaliação de todos os vizinhos
vizinhos_avaliacao = obter_avaliacao_vizinhos(vizinhos, mochila, capacidade_maxima, max_vizinhos)
# obtém a posição do melhor vizinho
pos_melhor_vizinho = obter_vizinho_melhor_avaliacao(vizinhos_avaliacao, lista_tabu, melhor_solucao, vizinhos)

# verifica se o melhor vizinho tem avaliação melhor do que a melhor avaliação até o momento
if vizinhos_avaliacao[pos_melhor_vizinho] > melhor_avaliacao:
	# obtém o bit que foi modificado do melhor vizinho
	bit_modificado = obter_bit_modificado(melhor_solucao, vizinhos[pos_melhor_vizinho])
	lista_tabu.append(bit_modificado) # guarda o movimento proibido
	melhor_solucao = vizinhos[pos_melhor_vizinho][:] # temos uma solução melhor, faz uma cópia
	melhor_iteracao += 1 # incrementa a iteração onde foi achada a melhor solução até o momento

iteracao += 1 # incrementa iteração

# Aqui terminou o PASSO 0, agora iremos entrar em loop (executar os outros passos)
while True:
	# a condição de parada é se a diferença da iteração e melhor_iteracao for maior que bt_max
	# iteracao é a iteração global (sempre é incrementada)
	# melhor_iteracao é a iteração onde se achou a melhor solução (nem sempre é incrementada)
	# bt_max é o máximo de iterações sem melhora no valor da melhor solução
	if (iteracao - melhor_iteracao) > bt_max:
		break
	# abaixo temos linhas de código quase idêntico ao PASSO 0
	# gerando novos vizinhos, faz uma cópia dos novos vizinhos
	vizinhos = gerar_vizinhos(melhor_solucao, max_vizinhos)[:]
	# obtém o valor de avaliação de todos os vizinhos (faz uma cópia)
	vizinhos_avaliacao = obter_avaliacao_vizinhos(vizinhos, mochila, capacidade_maxima, max_vizinhos)[:]
	# obtém a posição do melhor vizinho
	pos_melhor_vizinho = obter_vizinho_melhor_avaliacao(vizinhos_avaliacao, lista_tabu, melhor_solucao, vizinhos)
	# verifica se o melhor vizinho tem avaliação melhor do que a melhor avaliação corrente
	if vizinhos_avaliacao[pos_melhor_vizinho] > melhor_avaliacao:
		# obtém o bit que foi modificado para gerar o melhor vizinho
		bit_modificado = obter_bit_modificado(melhor_solucao, vizinhos[pos_melhor_vizinho])
		lista_tabu[0] = bit_modificado # guarda o movimento proibido (Essa linha NÃO existia no Passo 0)
		melhor_solucao = vizinhos[pos_melhor_vizinho][:] # temos uma solução melhor, faz uma cópia da lista
		melhor_avaliacao = vizinhos_avaliacao[pos_melhor_vizinho] # atualiza a melhor avaliação
		melhor_iteracao += 1 # incrementa a iteração onde foi achada a melhor solução (nem sempre é incrementada)
	iteracao += 1 # incremento da iteração (sempre é incrementada)

# mostra a solução final e sua avaliação
print('Solução final: {0}, Avaliação: {1}'.format(melhor_solucao, obter_avaliacao(melhor_solucao, mochila, capacidade_maxima)))
print('Melhor iteração: {0}'.format(melhor_iteracao)) # mostra a iteração onde foi achada a melhor solução
print('Iteração: {0}'.format(iteracao)) # mostra a iteração global
