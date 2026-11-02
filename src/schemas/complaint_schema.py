COMPLAINT_REGISTER_TOOL = {
    "type": "function",
    "name": "register_customer_complaint",
    "description": (
        "Registra uma reclamação de cliente para análise da equipe "
        "responsável. Utilize somente após coletar todos os campos "
        "obrigatórios. O registro não aprova trocas, devoluções ou "
        "reembolsos e não envia notificações externas."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "customer_name": {
                "type": "string",
                "description": "Nome completo do cliente.",
            },
            "phone": {
                "type": "string",
                "description": "Telefone de contato informado pelo cliente.",
            },
            "email": {
                "type": "string",
                "description": "E-mail de contato informado pelo cliente.",
            },
            "product_name": {
                "type": "string",
                "description": "Nome do produto relacionado à reclamação.",
            },
            "purchase_date": {
                "type": "string",
                "description": "Data da compra informada pelo cliente.",
            },
            "description": {
                "type": "string",
                "description": "Descrição objetiva do problema relatado.",
            },
            "order_number": {
                "type": "string",
                "description": "Número do pedido, se informado pelo cliente.",
            },
        },
        "required": [
            "customer_name",
            "phone",
            "email",
            "product_name",
            "purchase_date",
            "description",
        ],
    },
}
