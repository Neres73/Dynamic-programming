# -*- coding: utf-8 -*-
"""
SAEDS - Sistema de Análise de Eventos via Satélite
Global Solution | Dynamic Programming (2ESPY)

Problema (Indústria Espacial):
    Uma constelação de satélites de observação da Terra envia, em tempo real,
    alertas de eventos ambientais (queimadas, enchentes, deslizamentos, etc.)
    para uma estação terrestre. Esses pacotes precisam ser processados na
    ordem em que chegam e, durante operações de emergência, o operador precisa
    localizar rapidamente um alerta específico pelo seu identificador.

Como a solução atende aos requisitos técnicos:
    - FILA (Queue/FIFO) ............ pipeline de processamento da telemetria.
    - PILHA (Stack/LIFO) ........... revisão dos eventos críticos detectados.
    - BUSCA BINÁRIA ................ localização de um alerta por ID.
    - RECURSIVIDADE ................ busca binária + contagem de críticos.
    - MODULARIZAÇÃO ................ toda a lógica encapsulada em funções (def).
"""

import json
import os
from collections import deque

ARQUIVO_DADOS = "dados_alertas.json"
LIMIAR_CRITICO = 4  # severidade >= 4 é considerada um evento crítico



# 1. CARREGAMENTO E MANIPULAÇÃO DE DADOS (arquivo externo .json)

def carregar_alertas(caminho):
    """Lê o arquivo JSON externo e devolve a lista de alertas (dicts)."""
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo '{caminho}' não encontrado.")
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def montar_fila(alertas):
    """
    Carrega os alertas em uma FILA (FIFO) na ordem de chegada.
    Usa collections.deque, que oferece remoção O(1) na frente da fila.
    """
    fila = deque()
    for alerta in alertas:
        fila.append(alerta)  # enfileira (entra no fim da fila)
    return fila



# 2. PROCESSAMENTO DA FILA (FIFO) + GERAÇÃO DA PILHA DE CRÍTICOS (LIFO)

def processar_fila(fila):
    """
    Processa a fila em ordem FIFO (o primeiro a chegar é o primeiro a sair),
    simulando o pipeline da estação terrestre.

    Retorna:
        relatorio       -> dict com a contagem de alertas por severidade
        pilha_criticos  -> PILHA (lista usada como LIFO) com os eventos críticos
    """
    relatorio = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    pilha_criticos = []  # lista usada como Pilha: append = push / pop = pop

    print("\n>>> Processando fila de telemetria (FIFO)...\n")
    posicao = 1
    while fila:
        alerta = fila.popleft()           # desenfileira (sai da frente -> FIFO)
        sev = alerta["severidade"]
        relatorio[sev] += 1
        marcador = "  <== CRÍTICO" if sev >= LIMIAR_CRITICO else ""
        print(f"  [{posicao:02d}] Alerta {alerta['id_alerta']} | "
              f"{alerta['satelite']:<11} | {alerta['tipo_evento']:<16} | "
              f"Sev {sev}{marcador}")
        if sev >= LIMIAR_CRITICO:
            pilha_criticos.append(alerta)  # empilha (push) o evento crítico
        posicao += 1

    print("\n>>> Fila totalmente processada.\n")
    return relatorio, pilha_criticos



# 3. ORDENAÇÃO + BUSCA BINÁRIA RECURSIVA

def ordenar_por_id(alertas):
    """Devolve uma nova lista ordenada por id_alerta (pré-requisito da busca binária)."""
    return sorted(alertas, key=lambda a: a["id_alerta"])


def busca_binaria_recursiva(lista_ordenada, id_alvo, inicio, fim):
    """
    BUSCA BINÁRIA implementada de forma RECURSIVA.
    Localiza um alerta pelo id_alerta em uma lista JÁ ordenada por id.

    Retorna o dicionário do alerta encontrado ou None.
    """
    # Caso base: intervalo vazio -> não encontrado
    if inicio > fim:
        return None

    meio = (inicio + fim) // 2
    id_meio = lista_ordenada[meio]["id_alerta"]

    if id_meio == id_alvo:
        return lista_ordenada[meio]                                   # achou
    elif id_alvo < id_meio:
        return busca_binaria_recursiva(lista_ordenada, id_alvo, inicio, meio - 1)  # esquerda
    else:
        return busca_binaria_recursiva(lista_ordenada, id_alvo, meio + 1, fim)     # direita


def contar_criticos_recursivo(alertas, indice=0):
    """
    Conta RECURSIVAMENTE quantos alertas são críticos (severidade >= LIMIAR_CRITICO).
    Demonstra recursividade em uma funcionalidade adicional do sistema.
    """
    if indice == len(alertas):  # caso base: percorreu toda a lista
        return 0
    atual = 1 if alertas[indice]["severidade"] >= LIMIAR_CRITICO else 0
    return atual + contar_criticos_recursivo(alertas, indice + 1)



# 4. APRESENTAÇÃO (interface de texto)

def exibir_alerta(alerta):
    """Imprime os detalhes completos de um alerta."""
    print("  " + "-" * 50)
    print(f"  ID do Alerta : {alerta['id_alerta']}")
    print(f"  Satélite     : {alerta['satelite']}")
    print(f"  Evento       : {alerta['tipo_evento']}")
    print(f"  Região       : {alerta['regiao']}")
    print(f"  Coordenadas  : ({alerta['latitude']}, {alerta['longitude']})")
    print(f"  Severidade   : {alerta['severidade']} / 5")
    print(f"  Sinal        : {alerta['status_sinal']}")
    print(f"  Timestamp    : {alerta['timestamp']}")
    print("  " + "-" * 50)


def exibir_menu():
    print("\n" + "=" * 54)
    print("   SAEDS - Análise de Eventos via Satélite")
    print("=" * 54)
    print("   1 - Processar fila de telemetria (FIFO)")
    print("   2 - Buscar alerta por ID (Busca Binária recursiva)")
    print("   3 - Revisar eventos críticos (Pilha / LIFO)")
    print("   4 - Estatísticas gerais (contagem recursiva)")
    print("   5 - Listar todos os alertas")
    print("   0 - Sair")
    print("=" * 54)



# 5. PROGRAMA PRINCIPAL

def main():
    try:
        alertas = carregar_alertas(ARQUIVO_DADOS)
    except (FileNotFoundError, json.JSONDecodeError) as erro:
        print(f"ERRO ao carregar os dados: {erro}")
        return

    print(f"\n[OK] {len(alertas)} alertas carregados de '{ARQUIVO_DADOS}'.")

    pilha_criticos = []  # mantém os críticos do último processamento

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            fila = montar_fila(alertas)
            relatorio, pilha_criticos = processar_fila(fila)
            print("Resumo por severidade:")
            for sev in sorted(relatorio):
                print(f"   Severidade {sev}: {relatorio[sev]} alerta(s)")
            print(f"\nEventos críticos empilhados: {len(pilha_criticos)}")

        elif opcao == "2":
            entrada = input("Digite o ID do alerta (ex: 1015): ").strip()
            if not entrada.isdigit():
                print("ID inválido. Digite apenas números.")
                continue
            id_alvo = int(entrada)
            ordenada = ordenar_por_id(alertas)  # busca binária exige lista ordenada
            resultado = busca_binaria_recursiva(ordenada, id_alvo, 0, len(ordenada) - 1)
            if resultado:
                print(f"\n[ACHADO] Alerta {id_alvo} localizado:")
                exibir_alerta(resultado)
            else:
                print(f"\n[NAO ENCONTRADO] Nenhum alerta com ID {id_alvo}.")

        elif opcao == "3":
            if not pilha_criticos:
                print("Nenhum evento crítico em memória. Execute a opção 1 primeiro.")
            else:
                print("\n>>> Revisando eventos críticos (LIFO - mais recente no topo):\n")
                copia = list(pilha_criticos)  # consome uma cópia p/ não perder o estado
                while copia:
                    alerta = copia.pop()      # desempilha (pop) -> ordem inversa
                    print(f"   [TOPO] Alerta {alerta['id_alerta']} - "
                          f"{alerta['tipo_evento']} (Sev {alerta['severidade']}) "
                          f"em {alerta['regiao']}")

        elif opcao == "4":
            total = len(alertas)
            criticos = contar_criticos_recursivo(alertas)  # recursividade
            print(f"\n   Total de alertas      : {total}")
            print(f"   Alertas críticos      : {criticos}")
            print(f"   Alertas não críticos  : {total - criticos}")

        elif opcao == "5":
            print()
            for a in alertas:
                print(f"   ID {a['id_alerta']:<5} | {a['satelite']:<11} | "
                      f"{a['tipo_evento']:<16} | Sev {a['severidade']} | {a['regiao']}")

        elif opcao == "0":
            print("\nEncerrando o sistema. Até logo!\n")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
