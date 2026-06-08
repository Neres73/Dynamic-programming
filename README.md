# 🛰️ SAEDS — Sistema de Análise de Eventos via Satélite

> **Global Solution — Dynamic Programming (2ESPY)**
> Estruturas de Dados no Ecossistema Espacial

Sistema em Python que processa, em memória, alertas de eventos ambientais
captados por uma constelação de satélites de observação da Terra, demonstrando
o uso eficiente de **estruturas de dados (Fila e Pilha)**, **busca binária** e
**recursividade**.

---

## 1. Definição do Problema

No ecossistema da **economia espacial**, satélites de observação da Terra
(Amazonia-1, CBERS-4A, Landsat, Sentinel, MODIS, NOAA, GOES, etc.) monitoram o
planeta 24h por dia e geram **alertas de eventos** — queimadas, enchentes,
deslizamentos, secas, desmatamento e tempestades.

Esses alertas chegam continuamente a uma **estação terrestre**, que precisa:

1. **Processar a telemetria na ordem em que chega** (o pacote mais antigo da
   fila deve ser tratado primeiro);
2. **Priorizar a revisão dos eventos críticos** (severidade alta), começando
   pelo mais recentemente detectado;
3. **Localizar rapidamente um alerta específico** pelo seu identificador,
   durante uma operação de emergência.

Resolver esse fluxo de forma eficiente ajuda a **antecipar desastres naturais e
salvar vidas**, que é exatamente o impacto positivo proposto pelo desafio.

---

## 2. Lógica de Resolução

Cada necessidade do problema foi mapeada para uma estrutura/algoritmo adequado:

| Necessidade do problema | Solução aplicada | Por quê |
|---|---|---|
| Processar telemetria na ordem de chegada | **Fila (Queue / FIFO)** com `collections.deque` | O primeiro a chegar é o primeiro a ser processado; `popleft()` é **O(1)** |
| Revisar eventos críticos do mais recente ao mais antigo | **Pilha (Stack / LIFO)** com `list` (`append`/`pop`) | Em emergências, o último evento crítico detectado é o mais urgente de revisar |
| Encontrar um alerta por ID | **Busca Binária** | Reduz a busca de **O(n)** para **O(log n)** sobre os dados ordenados |
| Implementar a busca de forma elegante | **Recursividade** | A busca binária divide o problema pela metade a cada chamada recursiva |

Toda a lógica está **encapsulada em funções (`def`)**, mantendo o código modular.

### Funções principais (`main.py`)

| Função | Responsabilidade |
|---|---|
| `carregar_alertas(caminho)` | Lê o arquivo externo **`dados_alertas.json`** |
| `montar_fila(alertas)` | Carrega os registros em uma **Fila (FIFO)** |
| `processar_fila(fila)` | Processa a fila em ordem FIFO e empilha os críticos em uma **Pilha (LIFO)** |
| `ordenar_por_id(alertas)` | Ordena por `id_alerta` (pré-requisito da busca binária) |
| `busca_binaria_recursiva(lista, alvo, inicio, fim)` | **Busca Binária Recursiva** — núcleo do requisito |
| `contar_criticos_recursivo(alertas, indice)` | Contagem **recursiva** adicional dos eventos críticos |
| `exibir_alerta` / `exibir_menu` / `main` | Interface de texto e laço principal |

---

## 3. Estrutura de Dados (base com 35 registros)

Os dados são carregados de um **arquivo externo JSON** (`dados_alertas.json`),
contendo **35 registros contínuos** (acima do mínimo de 30 exigido). Cada
registro representa um alerta de satélite:

```json
{
  "id_alerta": 1015,
  "satelite": "Sentinel-1A",
  "tipo_evento": "DESMATAMENTO",
  "regiao": "Oceano Atlantico - Costa NE",
  "latitude": -5.4299,
  "longitude": -34.9006,
  "severidade": 5,
  "status_sinal": "INTERMITENTE",
  "timestamp": "2025-05-31T08:34:00Z"
}
```

> 💡 No arquivo, os registros estão na **ordem de chegada** (timestamp
> crescente), mas com os **IDs propositalmente embaralhados**. Isso torna a
> ordenação **obrigatória** antes da busca binária — evidenciando, na prática,
> por que o algoritmo exige uma lista ordenada.

Um alerta com `severidade >= 4` é tratado como **crítico**.

---

## 4. Algoritmo de Busca + Recursividade

A localização de um alerta usa **Busca Binária implementada com Recursividade**:

```python
def busca_binaria_recursiva(lista_ordenada, id_alvo, inicio, fim):
    if inicio > fim:                       # caso base: não encontrado
        return None
    meio = (inicio + fim) // 2
    id_meio = lista_ordenada[meio]["id_alerta"]
    if id_meio == id_alvo:
        return lista_ordenada[meio]        # encontrado
    elif id_alvo < id_meio:
        return busca_binaria_recursiva(lista_ordenada, id_alvo, inicio, meio - 1)
    else:
        return busca_binaria_recursiva(lista_ordenada, id_alvo, meio + 1, fim)
```

A cada chamada recursiva o intervalo de busca é dividido pela metade, resultando
em complexidade **O(log n)**.

---

## 5. Como Executar

**Pré-requisitos:** Python 3.x (utiliza apenas a **biblioteca padrão** — não há
dependências externas a instalar).

```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/<seu-repositorio>.git
cd <seu-repositorio>

# 2. Execute o sistema
python main.py
```

### Menu interativo

```
1 - Processar fila de telemetria (FIFO)
2 - Buscar alerta por ID (Busca Binária recursiva)
3 - Revisar eventos críticos (Pilha / LIFO)
4 - Estatísticas gerais (contagem recursiva)
5 - Listar todos os alertas
0 - Sair
```

> Dica de teste: execute a opção **1** (processa a fila e monta a pilha de
> críticos), depois a **2** buscando um ID válido (ex.: `1015`) e um inexistente
> (ex.: `9999`), e por fim a **3** para ver a pilha sendo desempilhada em ordem
> LIFO.

---

## 6. Estrutura do Repositório

```
.
├── main.py              # Programa principal (Fila, Pilha, Busca Binária, Recursão)
├── dados_alertas.json   # Base de dados externa com 35 registros
└── README.md            # Esta documentação
```

---

## 7. Checklist dos Requisitos Atendidos

- [x] Problema real alinhado à **Indústria Espacial**
- [x] Dados carregados de **arquivo externo** (`.json`) com **35 registros** (≥ 30)
- [x] Dados gerenciados em memória com **Fila (FIFO)** e **Pilha (LIFO)**
- [x] **Busca Binária** para localizar um registro pelo ID
- [x] Busca central resolvida com **Recursividade**
- [x] Código modular, todo encapsulado em **funções (`def`)**
- [x] Documentação no **README.md** e entrega via **GitHub**
