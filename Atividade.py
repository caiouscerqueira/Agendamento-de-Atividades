import time
import random

class Atividade:
    def __init__(self, codigo, nome, inicio, fim, prioridade, participantes):
        self.codigo = codigo
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self.prioridade = prioridade
        self.participantes = participantes

    def __repr__(self):
        return f"[Cod: {self.codigo}] {self.nome: <10} | Horário: {self.inicio:0>2}:00-{self.fim:0>2}:00 | Part: {self.participantes}"

# IMPLEMENTAÇÃO OBRIGATÓRIA: MERGE SORT (Dividir para Conquistar)
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

# ESTRATÉGIA GULOSA: Foco em Quantidade Máxima
def selecao_gulosa(atividades):
    atividades_copy = atividades[:]
    merge_sort(atividades_copy, 'fim') # Ordenação obrigatória por fim
    
    # Ajuste na geração de dados para garantir que fim seja maior que início
    # Caso contrário, nenhuma atividade pode ser selecionada
    selecionadas = []
    if not atividades_copy:
        return selecionadas

    ultima_fim = -1
    for act in atividades_copy:
        if act.inicio >= ultima_fim:
            selecionadas.append(act)
            ultima_fim = act.fim
            
    return selecionadas

# PROGRAMAÇÃO DINÂMICA: Foco em Benefício Máximo (Participantes)
def selecao_dp(atividades):
    atividades_copy = atividades[:]
    merge_sort(atividades_copy, 'fim')
    n = len(atividades_copy)
    if n == 0: return 0, []
    
    # Função para encontrar a última atividade compatível
    def busca_compativel(lista, i):
        for j in range(i - 1, -1, -1):
            if lista[j].fim <= lista[i].inicio:
                return j
        return -1

    # CORREÇÃO: Inicialização correta da tabela DP
    table = [0] * n 
    table[0] = atividades_copy[0].participantes # Pega participantes do primeiro objeto corretamente
    
    # Lista para rastrear quais atividades compõem a solução ótima
    selecionadas_list = [[] for _ in range(n)]
    selecionadas_list[0] = [atividades_copy[0]]
    
    for i in range(1, n):
        # Opção 1: Incluir a atividade atual
        beneficio_incluindo = atividades_copy[i].participantes
        j = busca_compativel(atividades_copy, i)
        if j != -1:
            beneficio_incluindo += table[j]
        
        # Opção 2: Excluir a atividade atual (pegar o melhor resultado anterior)
        beneficio_excluindo = table[i-1]
        
        if beneficio_incluindo > beneficio_excluindo:
            table[i] = beneficio_incluindo
            selecionadas_list[i] = (selecionadas_list[j] if j != -1 else []) + [atividades_copy[i]]
        else:
            table[i] = beneficio_excluindo
            selecionadas_list[i] = selecionadas_list[i-1]
    
    return table[n-1], selecionadas_list[n-1]

# CONJUNTOS DE TESTE OBRIGATÓRIOS
def gerar_dados(n):
    # CORREÇÃO LÓGICA: O horário de 'fim' deve ser gerado com base no horário de 'inicio'
    # Se início for sorteado como 18h e fim como 11h, a atividade seria inválida.
    dados = []
    for i in range(n):
        inicio = random.randint(8, 17)
        fim = random.randint(inicio + 1, 22) # Garante que o fim é depois do início
        dados.append(Atividade(i+1, f"Ativ_{i+1}", inicio, fim, random.randint(1,5), random.randint(10,100)))
    return dados

def executar_sistema():
    print("INSTITUTO DE COMPUTAÇÃO - UFBA")
    print("Sistema de Agendamento de Atividades - Testes Operacionais\n")
    
    cenarios = [("Pequeno", 8), ("Médio", 15), ("Maior", 35)]
    
    for nome, qtd in cenarios:
        print(f"{'='*20} TESTE {nome.upper()} ({qtd} atividades) {'='*20}")
        dados = gerar_dados(qtd)
        
        start = time.time()
        
        # Teste Guloso
        gulosa = selecao_gulosa(dados)
        print(f"Gulosa (Foco Qtd): {len(gulosa)} atividades selecionadas.")
        
        # Teste DP
        valor_dp, itens_dp = selecao_dp(dados)
        print(f"P. Dinâmica (Foco Partic.): {valor_dp} participantes em {len(itens_dp)} atividades.")
        
        print(f"Tempo de execução: {time.time() - start:.5f}s\n")

if __name__ == "__main__":
    executar_sistema()
