# CRM — Sprint 3: Recursão e Memoização

> **Dynamic Programming aplicado a um sistema de CRM médico.**  
> Verificação de leads duplicados e otimização de agenda usando recursão e memoização.

---

## Integrantes
- Luis Filipe Crivellaro – RM: 560877
- Felipe Silva do Prado Lima – RM: 559848
- Rafael Mandel – RM: 560333

---

## Sumário

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Verificação Recursiva de Duplicidade](#verificação-recursiva-de-duplicidade)
- [Memoização](#memoização)
- [Otimização de Agenda](#otimização-de-agenda)
- [Complexidade Algorítmica](#complexidade-algorítmica)

---

## Visão Geral

Quando novos leads chegam ao sistema, eles podem já existir no banco de dados. O sistema verifica duplicidade com base em **nome, telefone, e-mail e CPF**. Além disso, o agendamento diário de consultas é otimizado para maximizar a prioridade atendida dentro dos slots disponíveis.

---

## Estrutura do Projeto

```
crm_dp/
├── main.py                              # Ponto de entrada
├── src/
│   ├── tarefa1_verificacao_recursiva.py # recursão pura
│   ├── tarefa2_memoizacao.py            # cache manual + lru_cache
│   └── tarefa3_otimizacao_agenda.py     # 0/1 Knapsack com memo
└──
```

---

## Como Executar

### Pré-requisitos

- Python 3.10 ou superior

### Instalação

```bash
git clone https://github.com/rflMandell/Sprint03-DP-2026
```

### Rodar todas as tarefas

```bash
python main.py
```

---

## Verificação Recursiva de Duplicidade

**Arquivo:** `src/verificacao_recursiva.py`

### Problema

Um lead é considerado duplicado se qualquer campo-chave (`nome`, `telefone`, `email`, `cpf`) coincidir com um cadastro existente.

### Solução

Função recursiva `verificar_duplicidade` que percorre a lista de cadastros:

- **Caso base:** índice ultrapassa o tamanho da lista → retorna `(False, None)`  
- **Caso recursivo:** compara os campos-chave do lead com o cadastro atual; se houver coincidência, retorna `(True, cadastro_duplicado)`; caso contrário, avança para o próximo índice.

```python
def verificar_duplicidade_recursiva(novo_lead, cadastros, indice=0):
    if indice >= len(cadastros):
        return False, None                          # base: lista esgotada

    if _campos_coincidem(novo_lead, cadastros[indice]):
        return True, cadastros[indice]              # duplicata encontrada

    return verificar_duplicidade_recursiva(         # recursão para próximo
        novo_lead, cadastros, indice + 1
    )
```

### Árvore de Recursão (exemplo)

```
verificar(lead, cadastros, 0)
  ├─ _campos_coincidem(lead, cadastros[0]) → False
  └─ verificar(lead, cadastros, 1)
       ├─ _campos_coincidem(lead, cadastros[1]) → True ✓
       └─ retorna (True, cadastros[1])
```

---

## Memoização

**Arquivo:** `src/verificacao_memoizacao.py`

### Problema

Em um lote de leads chegando em sequência, o mesmo lead pode ser submetido mais de uma vez ou dois leads podem compartilhar campos similares — gerando comparações redundantes.

### Solução: duas abordagens

#### A) Cache manual com dicionário (`VerificadorComMemo`)

Cada par `(lead, índice_cadastro)` gera uma chave única. O resultado da comparação é armazenado e recuperado sem reexecutar a lógica.

```python
chave = f"{valores_lead}::{indice_cadastro}"

if chave in self.cache:
    self.hits += 1
    return self.cache[chave]          # cache hit → zero custo

resultado = _comparar_campos(...)     # cache miss → computa
self.cache[chave] = resultado
```

#### B) Decorador `@lru_cache` da stdlib

Versão pythônica: converte leads em tuplas hasháveis e delega o cache ao `functools.lru_cache`.

```python
@lru_cache(maxsize=512)
def _comparar_leads_cached(chave_lead, chave_cadastro):
    ...
```

### Resultado típico

| Métrica              | Valor     |
|----------------------|-----------|
| Comparações totais   | 15        |
| Cache hits           | 6         |
| Economia             | 40 %      |

---

## Otimização de Agenda

**Arquivo:** `src/otimizacao_agenda.py`

### Problema

O médico possui **20 slots** de 30 minutos (8h–18h). Há 12 consultas na fila, cada uma com uma duração e uma prioridade. Queremos maximizar a soma de prioridades sem exceder a capacidade do dia.

### Modelagem

Equivalente ao **Problema da Mochila 0/1 (0/1 Knapsack)**:

| Conceito da mochila | Equivalente no CRM      |
|---------------------|-------------------------|
| Capacidade          | Slots disponíveis       |
| Item                | Consulta                |
| Peso do item        | Duração (em slots)      |
| Valor do item       | Prioridade/urgência     |

### Solução

Recursão com memoização pelo par de estado `(indice, slots_restantes)`:

```python
def otimizar(self, consultas, slots, indice=0):
    if indice >= len(consultas) or slots <= 0:
        return 0, []                      # caso base

    estado = (indice, slots)
    if estado in self.memo:
        return self.memo[estado]          # memo hit

    # Opção 1: pula esta consulta
    v_sem, a_sem = self.otimizar(consultas, slots, indice + 1)

    # Opção 2: inclui esta consulta (se couber)
    v_com, a_com = 0, []
    if consultas[indice].duracao <= slots:
        v, a = self.otimizar(consultas,
                             slots - consultas[indice].duracao,
                             indice + 1)
        v_com = consultas[indice].valor + v
        a_com = [consultas[indice]] + a

    resultado = (v_com, a_com) if v_com >= v_sem else (v_sem, a_sem)
    self.memo[estado] = resultado
    return resultado
```

### Exemplo de saída

```
Valor total maximizado : 48 pontos de prioridade

  08:00–09:00  | Carla Mendes         | prioridade=9
  09:00–10:00  | Gabriela Nunes       | prioridade=9
  10:00–11:00  | Karla Vieira (120m)  | prioridade=10
  ...

Desempenho do otimizador:
   Chamadas recursivas : 147
   Cache hits          : 89
   Economia            : 60.5%
   Redução vs bruta    : 94.3%
```

---

## Complexidade Algorítmica

| Tarefa | Tempo         | Espaço       |
|--------|---------------|--------------|
| 1      | O(n × k)      | O(n)         |
| 2      | O(n × k) *    | O(n × k)     |
| 3      | O(n × S)      | O(n × S)     |

> \* Cada par único é computado apenas uma vez. `n` = nº de cadastros, `k` = nº de campos-chave, `S` = slots totais do dia.

---

## Conceitos de Dynamic Programming Aplicados

| Conceito               | Onde aparece                               |
|------------------------|--------------------------------------------|
| Recursão com caso base | Todas as tarefas                           |
| Memoização top-down    | Tarefas 2 e 3                              |
| Subproblemas sobrepostos | Tarefa 3 (mesmos estados reaparecem)     |
| Subestrutura ótima     | Tarefa 3 (solução global = ótimos locais) |

---

*Sprint 3 — Dynamic Programming | CRM System*