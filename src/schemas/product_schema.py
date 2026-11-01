PRODUCT_SEARCH_TOOL = {
    "type": "function",
    "name": "search_store_products",
    "description": (
        "Pesquisa produtos do Empório da Música por nome, categoria, "
        "descrição ou especificações. Retorna nome, descrição, preço, "
        "estoque, disponibilidade e promoções aplicáveis. Use esta "
        "ferramenta para perguntas sobre produtos, preços e disponibilidade. "
        "Não invente informações nem recalcule os preços retornados. "
        "A consulta retorna no máximo cinco produtos."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "Nome ou termos relacionados ao produto procurado " "pelo cliente."
                ),
            }
        },
        "required": ["query"],
    },
}
