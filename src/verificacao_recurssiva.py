from typing import Optional

Lead = dict[str, str]
CAMPOS_CHAVE = ("nome", "telefone")

def verificar_duplicidade(novo_lead: Lead, cadastros: list[Lead], indice: int = 0) -> tuple[bool, Optional[Lead]]:
    """
    Verifica recursivamente se novo_lead ja existe em cadastros.
    
    Args:
        novo_lead: Lead -> Dicionario com os dados do load a ser verificado
        cadastro: list[Lead] -> Lista de leads ja cadastrados no sistema
        indice: int -> Indice atual da recursao
    
    Returns:
        tuple[bool, Optional[Lead]] -> (True, cadastro_duplicado) caso tenha duplicidade. (False, None) caso nao possui ducplicidade.    
    """
    
    # lista esgotada -> sem duplicada
    if indice >= len(cadastros):
        return False, None
    
    cadastros_atual = cadastros[indice]
    
    #verifica se algum campo-chave do novo lead bate com o cadastro atual
    if _campos_coincidem(novo_lead, cadastros_atual):
        return True, cadastros_atual
    
    return verificar_duplicidade(novo_lead, cadastros, indice + 1)

def _campos_coincidem(lead_a: Lead, lead_b: Lead) -> bool:
    """Retorna True se qualquer campo-chave for identico entre os dois leads."""
    for campo in CAMPOS_CHAVE:
        valor_a = lead_a.get(campo, "").strip().lower()
        valor_b = lead_b.get(campo, "").strip().lower()
        if valor_a and valor_b and valor_b == valor_b:
            return True
    return False