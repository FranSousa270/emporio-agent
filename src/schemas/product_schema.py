PRODUCT_SEARCH_TOOL = {
    "type": "function",
    "name": "search_store_products",
    "description": (
        "Pesquisa produtos do Empório da Música por nome, descrição "
        "ou especificações. Retorna nome, descrição, preço, estoque, "
        "disponibilidade e promoções aplicáveis. Use esta ferramenta "
        "para perguntas sobre produtos, preços e disponibilidade. "
        "Não invente informações nem recalcule os preços retornados. "
        "Retorna no máximo cinco produtos por página. Para continuar "
        "uma pesquisa anterior, mantenha a mesma consulta e informe "
        "o número da próxima página, desde que existam mais resultados."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "Nome ou termos relacionados ao produto procurado " "pelo cliente."
                ),
            },
            "page": {
                "type": "integer",
                "minimum": 1,
                "description": (
                    "Número da página da pesquisa. Utilize 1 para uma "
                    "nova pesquisa e avance uma página por vez quando "
                    "o cliente solicitar mais resultados."
                ),
            },
        },
        "required": ["query"],
    },
}
