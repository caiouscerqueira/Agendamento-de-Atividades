import time
import random

# ═══════════════════════════════════════════════════════════════════
#  INSTITUTO DE COMPUTAÇÃO - UFBA
#  Análise e Projeto de Algoritmos
#  Sistema de Agendamento — Gulosa vs. Programação Dinâmica
# ═══════════════════════════════════════════════════════════════════

class Atividade:
    def __init__(self, codigo, nome, inicio, fim, prioridade, participantes):
        self.codigo      = codigo
        self.nome        = nome
        self.inicio      = inicio
        self.fim         = fim
        self.prioridade  = prioridade
        self.participantes = participantes

    def __repr__(self):
        barra = gerar_barra_horario(self.inicio, self.fim)
        return (f"  [{self.codigo:>2}] {self.nome:<12} "
                f"{self.inicio:02d}h-{self.fim:02d}h  "
                f"{barra}  {self.participantes:>3} part.")


# ───────────────────────────────────────────────────────────────────
#  MERGE SORT  (Dividir para Conquistar — obrigatório)
# ───────────────────────────────────────────────────────────────────

def merge_sort(lista, chave):
    if len(lista) > 1:
        meio = len(lista) // 2
        esq  = lista[:meio]
        dir  = lista[meio:]

        merge_sort(esq, chave)
        merge_sort(dir, chave)

        i = j = k = 0
        while i < len(esq) and j < len(dir):
            if getattr(esq[i], chave) <= getattr(dir[j], chave):
                lista[k] = esq[i]; i += 1
            else:
                lista[k] = dir[j]; j += 1
            k += 1
        while i < len(esq):
            lista[k] = esq[i]; i += 1; k += 1
        while j < len(dir):
            lista[k] = dir[j]; j += 1; k += 1


# ───────────────────────────────────────────────────────────────────
#  ESTRATÉGIA GULOSA — maximiza quantidade de atividades
#  Critério: ordenar por horário de fim (earliest deadline first)
#  Complexidade: O(n log n)
# ───────────────────────────────────────────────────────────────────

def selecao_gulosa(atividades):
    atividades_copy = atividades[:]
    merge_sort(atividades_copy, 'fim')

    selecionadas = []
    ultima_fim   = -1
    for act in atividades_copy:
        if act.inicio >= ultima_fim:
            selecionadas.append(act)
            ultima_fim = act.fim
    return selecionadas


# ───────────────────────────────────────────────────────────────────
#  PROGRAMAÇÃO DINÂMICA — maximiza participantes (benefício)
#  Subproblema: dp[i] = max participantes usando atividades 0..i
#  Recorrência: dp[i] = max(dp[i-1],  part[i] + dp[compat(i)])
#  Complexidade: O(n²)  — O(n log n) com busca binária
# ───────────────────────────────────────────────────────────────────

def selecao_dp(atividades):
    atividades_copy = atividades[:]
    merge_sort(atividades_copy, 'fim')
    n = len(atividades_copy)
    if n == 0:
        return 0, []

    def busca_compativel(lista, i):
        """Retorna índice da última atividade que termina <= inicio[i]."""
        for j in range(i - 1, -1, -1):
            if lista[j].fim <= lista[i].inicio:
                return j
        return -1

    dp   = [0] * n
    rast = [[] for _ in range(n)]          # rastreamento do caminho ótimo

    dp[0]   = atividades_copy[0].participantes
    rast[0] = [atividades_copy[0]]

    for i in range(1, n):
        j = busca_compativel(atividades_copy, i)

        incluindo = atividades_copy[i].participantes + (dp[j] if j != -1 else 0)
        excluindo = dp[i - 1]

        if incluindo > excluindo:
            dp[i]   = incluindo
            rast[i] = (rast[j] if j != -1 else []) + [atividades_copy[i]]
        else:
            dp[i]   = excluindo
            rast[i] = rast[i - 1]

    return dp[n - 1], rast[n - 1]


# ───────────────────────────────────────────────────────────────────
#  VISUALIZAÇÃO NO TERMINAL
# ───────────────────────────────────────────────────────────────────

HORA_INICIO = 8
HORA_FIM    = 20
LARGURA     = 36   # colunas da barra de horário


def gerar_barra_horario(inicio, fim, marcado=False):
    """Gera uma barra ASCII proporcional ao intervalo [inicio, fim]."""
    total  = HORA_FIM - HORA_INICIO
    col_s  = round((inicio - HORA_INICIO) / total * LARGURA)
    col_e  = round((fim    - HORA_INICIO) / total * LARGURA)
    bloco  = '█' if marcado else '▒'
    barra  = ' ' * col_s + bloco * max(1, col_e - col_s) + ' ' * (LARGURA - col_e)
    return f"|{barra}|"


def linha_tempo():
    """Régua de horas proporcional à barra."""
    total   = HORA_FIM - HORA_INICIO
    horas   = range(HORA_INICIO, HORA_FIM + 1, 2)
    marcas  = {}
    for h in horas:
        pos = round((h - HORA_INICIO) / total * LARGURA)
        marcas[pos] = str(h)

    ruler = ''
    i = 0
    while i <= LARGURA:
        if i in marcas:
            ruler += marcas[i]
            i     += len(marcas[i])
        else:
            ruler += ' '
            i     += 1
    return f" {'':14}  {'':5}  |{ruler[:LARGURA]}|"


def imprimir_atividades(lista, selecionadas_ids, simbolo):
    """Imprime cada atividade destacando as selecionadas."""
    ids_sel = {a.codigo for a in selecionadas_ids}
    for a in sorted(lista, key=lambda x: x.inicio):
        marcado = a.codigo in ids_sel
        barra   = gerar_barra_horario(a.inicio, a.fim, marcado)
        sel     = simbolo if marcado else ' '
        print(f"  {sel} [{a.codigo:>2}] {a.nome:<12} "
              f"{a.inicio:02d}h-{a.fim:02d}h  {barra}  {a.participantes:>3} part.")


def imprimir_resultado(titulo, atividades, gulosa, valor_dp, itens_dp):
    SEP = '─' * 68

    part_gulosa = sum(a.participantes for a in gulosa)
    part_dp     = valor_dp
    ganho       = part_dp - part_gulosa
    troca       = len(gulosa) - len(itens_dp)

    print(f"\n╔{'═'*66}╗")
    print(f"║  {titulo:<64}║")
    print(f"╚{'═'*66}╝")
    print(linha_tempo())
    print(f"  {SEP}")

    print(f"\n  ► GULOSA  (earliest deadline first — maximiza quantidade)")
    imprimir_atividades(atividades, gulosa, '●')
    print(f"  {SEP}")
    print(f"  Resultado: {len(gulosa)} atividades  |  {part_gulosa} participantes")

    print(f"\n  ► PROG. DINÂMICA  (weighted job scheduling — maximiza participantes)")
    imprimir_atividades(atividades, itens_dp, '●')
    print(f"  {SEP}")
    print(f"  Resultado: {len(itens_dp)} atividades  |  {part_dp} participantes")

    print(f"\n  ▶ COMPARATIVO")
    if ganho > 0:
        pct = ganho / part_gulosa * 100 if part_gulosa else 0
        sinal_troca = f"sacrificou {troca} ativ." if troca > 0 else "mesma quantidade"
        print(f"  DP atende {ganho} participantes a mais (+{pct:.0f}%)  [{sinal_troca}]")
        print(f"  Gulosa foi ótima em slots; DP foi ótima em impacto.")
    elif ganho == 0:
        print(f"  Ambos encontraram a mesma solução neste cenário.")
    else:
        print(f"  Gulosa superou a DP em participantes (incomum — verifique os dados).")
    print()


# ───────────────────────────────────────────────────────────────────
#  CASOS DE TESTE DETERMINÍSTICOS
# ───────────────────────────────────────────────────────────────────

def caso_classico():
    """
    Caso 1 — Contraste absoluto.

    Três atividades curtas (10 part.) cobrem 08h–14h em sequência.
    Uma atividade "lotada" (200 part.) ocupa exatamente o mesmo bloco.

    Gulosa: seleciona as 3 curtas (3 slots, 30 part.)  ← ótimo em qtd.
    DP    : descarta as 3 e fica com a lotada (1 slot, 200 part.)

    Lição: quando uma atividade vale mais que todas as menores juntas,
           a heurística gulosa falha completamente.
    """
    return [
        Atividade(1, "Curta-1",   8, 10, 1,  10),
        Atividade(2, "Curta-2",  10, 12, 1,  10),
        Atividade(3, "Curta-3",  12, 14, 1,  10),
        Atividade(4, "Lotada",    8, 14, 1, 200),
    ]


def caso_intermediario():
    """
    Caso 2 — Tradeoff realista.

    A3 (11h–12h, 15 part.) termina antes de A2 (10h–13h, 80 part.),
    então a gulosa a inclui — liberando A4 logo depois.
    Mas perde A2 com 80 participantes no processo.

    Gulosa: A1 + A3 + A4 + A5 + A6 = 5 ativ., 175 part.
    DP    : A1 + A2      + A5 + A6 = 4 ativ., 220 part.

    Lição: a gulosa paga um custo local pequeno (A3=15) para ganhar
           um slot, mas esse slot (A4=20) não compensa a perda de A2=80.
    """
    return [
        Atividade(1, "A1",  8, 10, 1,  20),
        Atividade(2, "A2", 10, 13, 1,  80),
        Atividade(3, "A3", 11, 12, 1,  15),
        Atividade(4, "A4", 12, 14, 1,  20),
        Atividade(5, "A5", 14, 17, 1,  90),
        Atividade(6, "A6", 17, 19, 1,  30),
    ]


def caso_cascata():
    """
    Caso 3 — Efeito cascata (erro se propaga por toda a grade).

    Quatro atividades curtas de baixo valor preenchem o dia.
    Três atividades de alto valor estão sobrepostas com elas, mas entre
    si são compatíveis — formam um caminho alternativo muito superior.

    Caminho guloso:  P1+P2+P3+P4 = 4 ativ., 60 part.
    Caminho ótimo:   V1+V2+V3    = 3 ativ., 270 part.

    Lição: um único erro guloso no começo bloqueia o caminho de maior
           valor para o resto do dia inteiro — o erro se propaga em cascata.
    """
    return [
        # Atividades "pequenas" — gulosa escolhe todas
        Atividade(1, "P1-manha",   8, 10, 1,  15),
        Atividade(2, "P2-manha",  10, 12, 1,  15),
        Atividade(3, "P3-tarde",  12, 15, 1,  15),
        Atividade(4, "P4-tarde",  15, 18, 1,  15),
        # Atividades "valiosas" — DP escolhe estas
        Atividade(5, "V1-manha",   8, 11, 1,  90),   # conflita com P1 e P2
        Atividade(6, "V2-tarde",  11, 15, 1,  90),   # conflita com P2 e P3
        Atividade(7, "V3-noite",  15, 19, 1,  90),   # conflita com P4
    ]


# ───────────────────────────────────────────────────────────────────
#  GERAÇÃO DE DADOS ALEATÓRIOS
# ───────────────────────────────────────────────────────────────────

def gerar_dados(n, semente=None):
    """
    Dados semi-controlados: duração curta (1-3h) para maximizar
    sobreposições; participantes com alto spread (5-200) para que
    a DP tenha motivo real para divergir da gulosa.
    """
    if semente is not None:
        random.seed(semente)
    dados = []
    for i in range(n):
        inicio       = random.randint(8, 17)
        fim          = random.randint(inicio + 1, min(inicio + 3, 20))
        participantes = random.randint(5, 200)
        dados.append(Atividade(i + 1, f"At{i+1:02d}", inicio, fim,
                               random.randint(1, 5), participantes))
    return dados


# ───────────────────────────────────────────────────────────────────
#  EXECUÇÃO PRINCIPAL
# ───────────────────────────────────────────────────────────────────

def executar_sistema():
    print("\n" + "═" * 68)
    print("  INSTITUTO DE COMPUTAÇÃO — UFBA")
    print("  Análise e Projeto de Algoritmos — Agendamento de Atividades")
    print("═" * 68)

    # ── Casos determinísticos ─────────────────────────────────────
    for fn, titulo in [
        (caso_classico,      "CASO 1 — Contraste absoluto (gulosa falha completamente)"),
        (caso_intermediario, "CASO 2 — Tradeoff realista  (gulosa boa, DP melhor)"),
        (caso_cascata,       "CASO 3 — Efeito cascata     (erro guloso se propaga)"),
    ]:
        dados    = fn()
        gulosa   = selecao_gulosa(dados)
        vdp, idp = selecao_dp(dados)
        imprimir_resultado(titulo, dados, gulosa, vdp, idp)

    # ── Casos aleatórios (escalabilidade) ─────────────────────────
    print("═" * 68)
    print("  TESTES ALEATÓRIOS — escalabilidade e comportamento médio")
    print("═" * 68)

    cenarios = [("Pequeno", 8, 7), ("Médio", 16, 13), ("Maior", 35, 99)]
    for nome, qtd, seed in cenarios:
        dados    = gerar_dados(qtd, semente=seed)
        start    = time.perf_counter()
        gulosa   = selecao_gulosa(dados)
        vdp, idp = selecao_dp(dados)
        elapsed  = time.perf_counter() - start

        part_g   = sum(a.participantes for a in gulosa)
        ganho    = vdp - part_g
        troca    = len(gulosa) - len(idp)

        print(f"\n  [{nome.upper()} — {qtd} atividades]")
        print(f"  Gulosa : {len(gulosa):2d} ativ. | {part_g:4d} part.")
        print(f"  DP     : {len(idp):2d} ativ. | {vdp:4d} part.", end="")
        if ganho > 0:
            print(f"  (+{ganho} part., {troca:+d} ativ.)")
        elif ganho == 0:
            print(f"  (mesma solução)")
        else:
            print()
        print(f"  Tempo  : {elapsed*1000:.3f} ms")

    print()


if __name__ == "__main__":
    executar_sistema()
