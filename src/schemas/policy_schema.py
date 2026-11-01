
POLICY_SEARCH_TOOL = {
    "type": "function",
    "name": "search_store_policies",
    "description": (
        "Consulta as políticas documentadas do Empório da Música. "
        "Use para dúvidas sobre horários, pagamentos, trocas, "
        "devoluções, garantia, entregas, promoções, reclamações "
        "e privacidade. Retorne apenas informações encontradas "
        "nas políticas. Esta ferramenta não aprova solicitações "
        "nem executa decisões da gerência."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "Termos relacionados à política que o cliente "
                    "deseja consultar. Exemplo: garantia de produto "
                    "com defeito."
                ),
            }
        },
        "required": ["query"],
    },
}
