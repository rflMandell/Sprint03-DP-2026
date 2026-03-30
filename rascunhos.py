from typing import Optional
from functools import lru_cache
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Modelo de dados
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Consulta:
    """Representa uma consulta a ser agendada."""
    id: str
    paciente: str
    duracao: int   # em slots de 30 min
    valor: int     # prioridade/importância (1–10)

    def __str__(self) -> str:
        horas = self.duracao * 30
        return (f"Consulta({self.id} | {self.paciente} | "
                f"{horas}min | prioridade={self.valor})")


# ---------------------------------------------------------------------------
# Solução com memoização explícita (dicionário)
# ---------------------------------------------------------------------------

class OtimizadorAgenda:
    """
    Otimiza o agendamento diário de um médico usando programação dinâmica
    recursiva com memoização.

    O estado do subproblema é definido por:
        (indice_consulta, slots_restantes)

    Isso garante que cada combinação seja calculada apenas uma vez.

    Atributos
    ----------
    memo : dict
        Cache de subproblemas resolvidos.
    chamadas_total : int
        Total de chamadas recursivas realizadas.
    chamadas_cache : int
        Chamadas atendidas pelo cache (sem recomputação).
    """

    def __init__(self) -> None:
        self.memo: dict[tuple[int, int], tuple[int, list[Consulta]]] = {}
        self.chamadas_total = 0
        self.chamadas_cache = 0

    def otimizar(
        self,
        consultas: tuple[Consulta, ...],
        slots_disponiveis: int,
        indice: int = 0,
    ) -> tuple[int, list[Consulta]]:
        """
        Calcula a combinação de consultas com maior valor total que
        caiba nos slots disponíveis do dia.

        Parâmetros
        ----------
        consultas         : tupla imutável de todas as consultas candidatas
        slots_disponiveis : slots ainda disponíveis na agenda
        indice            : índice atual na lista de consultas

        Retorno
        -------
        tuple[int, list[Consulta]]
            (valor_maximo, lista_de_consultas_selecionadas)

        Complexidade (com memoização)
        -----------------------------
        Tempo  : O(n * S)  — n consultas, S slots totais
        Espaço : O(n * S)  — tamanho do cache
        """
        self.chamadas_total += 1

        # Caso base: sem mais consultas ou agenda cheia
        if indice >= len(consultas) or slots_disponiveis <= 0:
            return 0, []

        # Verifica cache
        estado = (indice, slots_disponiveis)
        if estado in self.memo:
            self.chamadas_cache += 1
            return self.memo[estado]

        consulta_atual = consultas[indice]

        # Opção 1: pular esta consulta
        valor_sem, agenda_sem = self.otimizar(consultas, slots_disponiveis, indice + 1)

        # Opção 2: incluir esta consulta (se couber)
        valor_com, agenda_com = 0, []
        if consulta_atual.duracao <= slots_disponiveis:
            v, ag = self.otimizar(
                consultas,
                slots_disponiveis - consulta_atual.duracao,
                indice + 1,
            )
            valor_com = consulta_atual.valor + v
            agenda_com = [consulta_atual] + ag

        # Escolhe a melhor opção
        if valor_com >= valor_sem:
            resultado = (valor_com, agenda_com)
        else:
            resultado = (valor_sem, agenda_sem)

        self.memo[estado] = resultado
        return resultado

    def exibir_estatisticas(self) -> None:
        economia = (
            self.chamadas_cache / self.chamadas_total * 100
            if self.chamadas_total else 0
        )
        print(f"\n  📊 Desempenho do otimizador:")
        print(f"     Chamadas recursivas : {self.chamadas_total}")
        print(f"     Cache hits          : {self.chamadas_cache}")
        print(f"     Economia            : {economia:.1f}%")
        print(f"     Subproblemas únicos : {len(self.memo)}")


# ---------------------------------------------------------------------------
# Utilitários de exibição
# ---------------------------------------------------------------------------

def exibir_agenda(consultas_selecionadas: list[Consulta], slots_totais: int) -> None:
    """Exibe a agenda otimizada de forma legible."""
    slots_usados = sum(c.duracao for c in consultas_selecionadas)
    minutos_usados = slots_usados * 30
    minutos_totais = slots_totais * 30

    print(f"\n  🗓️  Agenda otimizada ({minutos_usados}min / {minutos_totais}min usados):")
    if not consultas_selecionadas:
        print("     Nenhuma consulta encaixada.")
        return

    hora_atual = 8 * 60  # começa às 08:00
    for c in consultas_selecionadas:
        h_ini = divmod(hora_atual, 60)
        hora_atual += c.duracao * 30
        h_fim = divmod(hora_atual, 60)
        print(
            f"     {h_ini[0]:02d}:{h_ini[1]:02d}–{h_fim[0]:02d}:{h_fim[1]:02d}"
            f"  | {c.paciente:<20} | prioridade={c.valor}"
        )


# ---------------------------------------------------------------------------
# Demonstração
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Agenda do dia: 8h às 18h = 600 min = 20 slots de 30 min
    SLOTS_DO_DIA = 20

    consultas_candidatas = (
        Consulta("C01", "Ana Souza",        duracao=2, valor=8),   # 60 min, alta prioridade
        Consulta("C02", "Bruno Lima",        duracao=1, valor=5),   # 30 min
        Consulta("C03", "Carla Mendes",      duracao=3, valor=9),   # 90 min, urgente
        Consulta("C04", "Diego Rocha",       duracao=2, valor=6),   # 60 min
        Consulta("C05", "Eva Pinto",         duracao=4, valor=7),   # 120 min
        Consulta("C06", "Felipe Castro",     duracao=1, valor=4),   # 30 min
        Consulta("C07", "Gabriela Nunes",    duracao=2, valor=9),   # 60 min, alta prioridade
        Consulta("C08", "Henrique Alves",    duracao=3, valor=6),   # 90 min
        Consulta("C09", "Isabela Torres",    duracao=1, valor=7),   # 30 min
        Consulta("C10", "João Fernandes",    duracao=2, valor=5),   # 60 min
        Consulta("C11", "Karla Vieira",      duracao=4, valor=10),  # 120 min, urgência máxima
        Consulta("C12", "Leonardo Batista",  duracao=1, valor=3),   # 30 min
    )

    print("=" * 65)
    print("TAREFA 3 — Otimização de Agenda com Subproblemas (DP)")
    print("=" * 65)
    print(f"\n  Slots disponíveis : {SLOTS_DO_DIA} ({SLOTS_DO_DIA * 30} min)")
    print(f"  Consultas na fila : {len(consultas_candidatas)}")

    otimizador = OtimizadorAgenda()
    valor_max, agenda_otimizada = otimizador.otimizar(consultas_candidatas, SLOTS_DO_DIA)

    print(f"\n  ✅ Valor total maximizado: {valor_max} pontos de prioridade")
    exibir_agenda(agenda_otimizada, SLOTS_DO_DIA)
    otimizador.exibir_estatisticas()

    # --- Comparação sem memoização (força bruta) ---
    print("\n  🔄 Comparação: sem memoização (força bruta)")
    chamadas_sem_memo = [0]

    def forca_bruta(consultas, slots, indice=0):
        chamadas_sem_memo[0] += 1
        if indice >= len(consultas) or slots <= 0:
            return 0, []
        c = consultas[indice]
        v_sem, a_sem = forca_bruta(consultas, slots, indice + 1)
        v_com, a_com = 0, []
        if c.duracao <= slots:
            v, a = forca_bruta(consultas, slots - c.duracao, indice + 1)
            v_com, a_com = c.valor + v, [c] + a
        return (v_com, a_com) if v_com >= v_sem else (v_sem, a_sem)

    forca_bruta(consultas_candidatas, SLOTS_DO_DIA)
    reducao = (1 - otimizador.chamadas_total / chamadas_sem_memo[0]) * 100
    print(f"     Chamadas sem memo : {chamadas_sem_memo[0]}")
    print(f"     Chamadas com memo : {otimizador.chamadas_total}")
    print(f"     Redução           : {reducao:.1f}%")