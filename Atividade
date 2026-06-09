import time
import random

# ESTRUTURA DE DADOS: Atividade [1, 4]
class Atividade:
    def __init__(self, codigo, nome, inicio, fim, prioridade, participantes):
        self.codigo = codigo
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self.prioridade = prioridade
        self.participantes = participantes

    def __repr__(self):
        return f"[Cod: {self.codigo}] {self.nome: <15} | Horário: {self.inicio:0>2}:00-{self.fim:0>2}:00 | Part: {self.participantes: <3} | Prio: {self.prioridade}"

# IMPLEMENTAÇÃO OBRIGATÓRIA: MERGE SORT [5-7]
# Utiliza o paradigma de "Dividir para Conquistar" para garantir complexidade O(n log n) [5, 8, 9].
def merge_sort(lista, chave):
    if len(lista) > 1:
        meio = len(lista) // 2
        esq = lista[:meio]
        dir = lista[meio:]

        merge_sort(esq, chave)
        merge_sort(dir, chave)

        i = j = k = 0
        while i < len(esq) and j < len(dir):
            if getattr(esq[i], chave) <= getattr(dir[j], chave):
                lista[k] = esq[i]
                i += 1
            else:
                lista[k] = dir[j]
                j += 1
            k += 1

        while i < len(esq):
            lista[k] = esq[i]
            i += 1
            k += 1

        while j < len(dir):
            lista[k] = dir[j]
            j += 1
            k += 1

# ESTRATÉGIA 1: ALGORITMO GULOSO (Seleção de Atividades Clássica) [1, 10-12]
# Objetivo: Selecionar o MAIOR NÚMERO possível de atividades sem conflito [1, 2].
# A escolha localmente ótima é selecionar a atividade que termina mais cedo [11, 12].
def selecao_gulosa(atividades):
    # A ordenação pelo horário de fim é essencial para a prova de corretude da estratégia gulosa [11, 13].
    atividades_copy = atividades[:]
    merge_sort(atividades_copy, 'fim')
    
    selecionadas = []
    if not atividades_copy:
        return selecionadas

    # Seleciona a primeira atividade (a que termina mais cedo)
    ultima_atividade = atividades_copy
    selecionadas.append(ultima_atividade)

    for i in range(1, len(atividades_copy)):
        # Se a atividade atual começa após ou no momento do fim da última selecionada [1, 4]
        if atividades_copy[i].inicio >= ultima_atividade.fim:
            selecionadas.append(atividades_copy[i])
            ultima_atividade = atividades_copy[i]
            
    return selecionadas

# ESTRATÉGIA 2: PROGRAMAÇÃO DINÂMICA (Weighted Interval Scheduling) [1, 12, 14-16]
# Objetivo: Maximizar o BENEFÍCIO TOTAL (ex: soma de participantes ou peso) [1, 17].
# Diferente do guloso, esta técnica evita o re-cálculo e busca o ótimo global considerando pesos [12, 16].
def selecao_dp(atividades):
    atividades_copy = atividades[:]
    merge_sort(atividades_copy, 'fim')
    n = len(atividades_copy)
    
    # Encontrar o último índice j < i que não conflita com a atividade i
    def busca_compativel(lista, i):
        for j in range(i - 1, -1, -1):
            if lista[j].fim <= lista[i].inicio:
                return j
        return -1

    # table[i] armazena o lucro/benefício máximo obtido considerando atividades até o índice i [12, 16].
    table =  * n
    table = atividades_copy.participantes
    
    # Lista para rastrear as atividades selecionadas no ótimo global
    selecionadas_indices = [[] for _ in range(n)]
    selecionadas_indices = [atividades_copy]

    for i in range(1, n):
        beneficio_atual = atividades_copy[i].participantes
        j = busca_compativel(atividades_copy, i)
        
        beneficio_incluindo = beneficio_atual + (table[j] if j != -1 else 0)
        beneficio_excluindo = table[i-1]

        if beneficio_incluindo > beneficio_excluindo:
            table[i] = beneficio_incluindo
            selecionadas_indices[i] = (selecionadas_indices[j] if j != -1 else []) + [atividades_copy[i]]
        else:
            table[i] = beneficio_excluindo
            selecionadas_indices[i] = selecionadas_indices[i-1]
    
    return table[n-1], selecionadas_indices[n-1]

# GERADOR DE DADOS PARA TESTES [1, 18]
def gerar_atividades(quantidade):
    lista = []
    for i in range(quantidade):
        inicio = random.randint(8, 18)
        fim = inicio + random.randint(1, 4)
        lista.append(Atividade(
            i + 1, 
            f"Atividade {i+1}", 
            inicio, 
            fim, 
            random.randint(1, 5), 
            random.randint(10, 100)
        ))
    return lista

# EXECUÇÃO DOS CONJUNTOS DE TESTE [1, 18]
def executar_sistema():
    testes = [
        ("PEQUENO", gerar_atividades(8)),
        ("MÉDIO", gerar_atividades(15)),
        ("MAIOR", gerar_atividades(35))
    ]

    for label, dados in testes:
        print(f"\n{'='*30} TESTE {label} {'='*30}")
        print(f"Total de Atividades Cadastradas: {len(dados)}")
        
        # Benchmarking de desempenho [1, 4]
        start_time = time.time()
        
        # Execução Gulosa
        res_guloso = selecao_gulosa(dados)
        print(f"\n>>> SOLUÇÃO GULOSA (Foco em Qtd Máxima):")
        print(f"Total de atividades selecionadas: {len(res_guloso)}")
        for a in res_guloso: print(f"  {a}")
        
        # Execução Programação Dinâmica
        beneficio_dp, itens_dp = selecao_dp(dados)
        print(f"\n>>> SOLUÇÃO P. DINÂMICA (Foco em Máximo de Participantes):")
        print(f"Benefício total (Participantes): {beneficio_dp}")
        print(f"Total de atividades selecionadas: {len(itens_dp)}")
        for a in itens_dp: print(f"  {a}")
        
        end_time = time.time()
        print(f"\nTempo de processamento: {end_time - start_time:.6f}s")

if __name__ == "__main__":
    executar_sistema()
