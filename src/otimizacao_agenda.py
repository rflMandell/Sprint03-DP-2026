from typing import Optional
from functools import lru_cache
from dataclasses import dataclass

#modelo de dados
@dataclass(frozen=True)
class Consulta:
    """Representa uma consulta a ser agendada"""
    id: str
    paciente: str
    duracao: int #em slots de 30 minitos
    valor: int # prioridade/importancia (1-10)
    
    def __str__(self) -> str:
        horas = self.duracao * 30
        return (f"Consulta({self.id} | {self.paciente} | "
                f"{horas}min | prioridade={self.valor})")
        


#solucao com memoizacao explicita (uso de dicts)
class OtimizadorAgenda:
    """
    Otimiza o agendamento duario de um medico usando programacao dinamica recursiva com memoizacao.
    
    O estado do subproblema e definido por:
    (indice_consulta, slots_restantes)
    
    Isso garante que cada combinacao seja calculada apenas uma vez
    """
    
    def __init__(self) -> None:
        self.memo: dict[tuple[int, int], tuple[int, list[Consulta]]] = {}
        self.chamadas_total = 0
        self.chamadas_cache = 0
        
    def otimizar(self, consultas: tuple[Consulta, ...], slots_disponiveis: int, indice: int=0) -> tuple[int, list[Consulta]]:
        """Calcula a combinacao de consultas com maior valor total que caiba nos slots disponiveis do dia"""
        
        self.chamadas_total += 1
        
        #caso base: sem mais consultas ou agenda cheia
        if indice >= len(consultas) or slots_disponiveis <= 0:
            return 0, []
        
        #verifica cache
        estado = (indice, slots_disponiveis)
        if estado in self.memo:
            self.chamadas_cache += 1
            return self.memo[estado]
        
        consulta_atual = consultas[indice]
        
        #opcao 1 -> pular esta consulta
        valor_sem, agenda_sem = self.otimizar(consultas[1:], slots_disponiveis)
        
        #opcao 2-> incluir esta consulta (se tiver espaco)
        valor_com, agenda_com = 0, []
        if consulta_atual.duracao <= slots_disponiveis:
            v, ag = self.otimizar(consultas, slots_disponiveis - consulta_atual.duracao, indice + 1)
            valor_com = consulta_atual.valor + v
            agenda_com = [consulta_atual] + ag
            
        #escolhe a melhor opcao
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
        print(f"\n Desempenho do otimizador:")
        print(f"Chamadas recursivas: {self.chamadas_total}")
        print(f"Cache hits: {self.chamadas_cache}")
        print(f"Economia: {economia:.1f}%")
        print(f"Subproblemas unicos: {len(self.memo)}")


#utilitarios de exibicao
def exibir_agenda(consultas_selecionadas: list[Consulta], slots_totais: int) -> None:
    """Exibe a agenda otimizada de forma legible."""
    slots_usados = sum(c.duracao for c in consultas_selecionadas)
    minutos_usados = slots_usados * 30
    minutos_totais = slots_totais * 30
    
    print(f"\n Agenda otimizada ({minutos_usados}min / {minutos_totais}min usados):")
    if not consultas_selecionadas:
        print("Nenhuma consulta encaixada.")
        return

    hora_atual = 8 * 60  # considerando q comeca às 08:00
    for c in consultas_selecionadas:
        h_ini = divmod(hora_atual, 60)
        hora_atual += c.duracao * 30
        h_fim = divmod(hora_atual, 60)
        print(
            f"{h_ini[0]:02d}:{h_ini[1]:02d}-{h_fim[0]:02d}:{h_fim[1]:02d}"
            f" | {c.paciente:<20} | prioridade={c.valor}"
        )