"""
CRM — Sprint 3: Recursão e Memoização
======================================
Ponto de entrada único para demonstrar as três tarefas.

Execute:
    python main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.verificacao_recurssiva import verificar_duplicidade
from src.verificacao_memo import VerificadorComMemo, verificar_com_lru_cache, _comparar_leads_cached
from src.otimizacao_agenda import Consulta, OtimizadorAgenda, exibir_agenda


def separador(titulo: str) -> None:
    print("\n" + "═" * 65)
    print(f"  {titulo}")
    print("═" * 65)


def main() -> None:
    # Verificação Recursiva de Duplicidade
    separador("TAREFA 1 — Verificação Recursiva de Duplicidade")

    cadastros = [
        {"nome": "Ana Souza",    "telefone": "11999990001", "email": "ana@email.com",   "cpf": "111.111.111-11"},
        {"nome": "Bruno Lima",   "telefone": "11999990002", "email": "bruno@email.com", "cpf": "222.222.222-22"},
        {"nome": "Carla Mendes", "telefone": "11999990003", "email": "carla@email.com", "cpf": "333.333.333-33"},
    ]

    novos_leads = [
        {"nome": "A. Souza",  "telefone": "11000000000", "email": "ana@email.com",   "cpf": "999.999.000-00"},
        {"nome": "Novo Nome", "telefone": "11000000001", "email": "novo@email.com",   "cpf": "222.222.222-22"},
        {"nome": "Delta",     "telefone": "11888880004", "email": "delta@email.com",  "cpf": "444.444.444-44"},
    ]

    for lead in novos_leads:
        dup, conflito = verificar_duplicidade(lead, cadastros)
        status = "DUPLICADO" if dup else "NOVO"
        print(f"  [{status}] {lead['email']:<25}", end="")
        if dup:
            campo = next(
                (c for c in ("nome", "telefone", "email", "cpf")
                if lead.get(c, "").lower() == conflito.get(c, "").lower()),
                None
            )
            if campo:
                print(f" → conflito no campo '{campo}'")
            else:
                print(" → duplicado, mas nenhum campo específico coincide")

    # Memoização
    separador("TAREFA 2 — Memoização (cache manual + lru_cache)")

    lote = [
        {"nome": "X1", "telefone": "11000000001", "email": "ana@email.com",   "cpf": "999.000.001-00"},
        {"nome": "X2", "telefone": "11000000002", "email": "novo2@email.com", "cpf": "222.222.222-22"},
        {"nome": "X1", "telefone": "11000000001", "email": "ana@email.com",   "cpf": "999.000.001-00"},  # repetido
        {"nome": "X3", "telefone": "11777770003", "email": "novo3@email.com", "cpf": "777.777.777-77"},
        {"nome": "X2", "telefone": "11000000002", "email": "novo2@email.com", "cpf": "222.222.222-22"},  # repetido
    ]

    print("\n  > Cache manual:")
    verificador = VerificadorComMemo()
    for lead in lote:
        dup, _ = verificador.verificar(lead, cadastros)
        status = "DUPLICADO" if dup else "NOVO"
        print(f"    [{status}] {lead['nome']}")
    verificador.exibir_estatisticas()

    print("\n  > @lru_cache:")
    for lead in lote:
        dup, _ = verificar_com_lru_cache(lead, cadastros)
        status = "DUPLICADO" if dup else "NOVO"
        print(f"    [{status}] {lead['nome']}")
    info = _comparar_leads_cached.cache_info()
    print(f"\n  lru_cache — hits={info.hits}, misses={info.misses}")

    # Otimização de Agenda
    separador("TAREFA 3 — Otimização de Agenda (0/1 Knapsack + Memo)")

    SLOTS = 20  # 8h às 18h = 20 slots de 30 min

    consultas = (
        Consulta("C01", "Ana Souza",       duracao=2,  valor=8),
        Consulta("C02", "Bruno Lima",       duracao=1,  valor=5),
        Consulta("C03", "Carla Mendes",     duracao=3,  valor=9),
        Consulta("C04", "Diego Rocha",      duracao=2,  valor=6),
        Consulta("C05", "Eva Pinto",        duracao=4,  valor=7),
        Consulta("C06", "Felipe Castro",    duracao=1,  valor=4),
        Consulta("C07", "Gabriela Nunes",   duracao=2,  valor=9),
        Consulta("C08", "Henrique Alves",   duracao=3,  valor=6),
        Consulta("C09", "Isabela Torres",   duracao=1,  valor=7),
        Consulta("C10", "João Fernandes",   duracao=2,  valor=5),
        Consulta("C11", "Karla Vieira",     duracao=4,  valor=10),
        Consulta("C12", "Leonardo Batista", duracao=1,  valor=3),
    )

    print(f"\n  Slots do dia  : {SLOTS} ({SLOTS * 30} min disponíveis)")
    print(f"  Consultas     : {len(consultas)} na fila")

    otimizador = OtimizadorAgenda()
    valor_max, agenda = otimizador.otimizar(consultas, SLOTS)

    print(f"\n  Valor total maximizado : {valor_max} pontos")
    exibir_agenda(agenda, SLOTS)
    otimizador.exibir_estatisticas()

    print("\n" + "═" * 65)
    print("  Execução concluída com sucesso.")
    print("═" * 65 + "\n")


if __name__ == "__main__":
    main()