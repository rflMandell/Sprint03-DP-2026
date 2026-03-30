from typing import Optional
from functools import lru_cache

Lead = dict[str, str]
CAMPOS_CHAVE = ("nome", "telefone", "email", "cpf")


#cache manual com dict
class VerificadorComMemo:
    """
    Verifica duplicidade de leads com memoizacao explicita
    """
    
    def __init__(self) -> None:
        self.cache: dict[str, Optional[str]] = {}
        self.hits = 0
        self.total_comparacoes = 0
    
    #interface publica
    def verificar (self, novo_lead: Lead, cadastros: list[Lead], indice: int = 0,) -> tuple[bool, Optional[Lead]]:
        """
        Verifica recursivamente com memoizacao se novo_lead ja existe
        
        Args:
            novo_lead: Lead
            cadastro: list[Lead]
            indice: int
            
        Returns:
            tuple[bool, Optional[Lead]]
        """
        
        if indice >= len(cadastros):
            return False, None
        cadastro_atual = cadastros[indice]
        campo_conflito = self._comparar_com_cache(novo_lead, cadastro_atual, indice)
        if campo_conflito:
            return True, cadastro_atual
        return self.verificar(novo_lead, cadastros, indice + 1)
    
    def exibir_estatisticas(self) -> None:
        print(f"Comparações totais: {self.total_comparacoes}")
        print(f"Cache hits: {self.hits}")
        economia = (self.hits / self.total_comparacoes * 100) if self.total_comparacoes else 0
        print(f"Economia: {economia:.1f}%")
        print(f"Entradas no cache: {len(self.cache)}")
        
    
    #logica interna
    
    def _chave_cache(self, lead: Lead, indice_cadastro: int) -> str:
        """
        Gera uma chave de cache unica para o par (lead, cadastro)
        A chave combina os valores dos campos-chave do lead com o indice do cadastro, garantindo o par
        """
        valores = "|".join(
            lead.get(c, "").strip().lower() for c in CAMPOS_CHAVE
        )
        return f"{valores}::{indice_cadastro}"
    
    def _comparar_com_cache(self, novo_lead: Lead, cadastro: Lead, indice: int,) -> Optional[str]:
        """
        Compara dois leads, consultando o cache antes de executar.
        """
        chave = self._chave_cache(novo_lead, indice)
        self.total_comparacoes += 1
        if chave in self.cache:
            self.hits += 1
            return self.cache[chave]
        #cache miss -> realiza comparacao real
        campo_conflito = None
        for campo in CAMPOS_CHAVE:
            v_novo = novo_lead.get(campo, "").strip().lower()
            v_cad = cadastro.get(campo, "").strip().lower()
            if v_novo and v_cad and v_novo == v_cad:
                campo_conflito = campo
                break
        self.cache[chave] = campo_conflito
        return campo_conflito
    


# outra maneira usando o @lru_cache

@lru_cache(maxsize=1024)
def _comparar_leads_cached(): # ainda tem q colocar os parametros
    """a"""