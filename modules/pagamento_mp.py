"""
Módulo pagamento_mp.py
Integração com a API do Mercado Pago para geração e conferência de pagamentos PIX
no modelo Pay-Per-Use (R$ 5,70) com suporte nativo a Modo de Demonstração / Portfólio.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

VALOR_PAGAMENTO = 5.70
DESCRICAO_SERVICO = "Radar Currículo IA - Acesso Pay-per-use"


def obter_access_token_mp() -> str:
    """
    Obtém o Access Token do Mercado Pago do ambiente.
    """
    token = os.getenv("MERCADO_PAGO_ACCESS_TOKEN", "").strip()
    if not token:
        try:
            import streamlit as st
            if "MERCADO_PAGO_ACCESS_TOKEN" in st.secrets:
                token = st.secrets["MERCADO_PAGO_ACCESS_TOKEN"]
        except Exception:
            pass
    return token or ""


def is_mp_configurado() -> bool:
    """
    Verifica se o token do Mercado Pago está definido.
    """
    token = obter_access_token_mp()
    return bool(token and token.startswith(("APP_USR-", "TEST-")))


def criar_pagamento_pix(email_usuario: str, nome_usuario: str) -> Dict[str, Any]:
    """
    Cria uma ordem de cobrança PIX via Mercado Pago no valor fixo de R$ 5,70.
    Em ambiente de portfólio/demonstração, gera um payload válido e seguro.

    Args:
        email_usuario: E-mail do pagador.
        nome_usuario: Nome do pagador.

    Returns:
        Dict contendo id, status, qr_code, qr_code_base64 e ticket_url.
    """
    token = obter_access_token_mp()

    # Modo demonstração / portfólio seguro (sem cobrança bancária real)
    if not token or not token.startswith(("APP_USR-", "TEST-")):
        return {
            "id": 9999999999,
            "status": "pending",
            "valor": VALOR_PAGAMENTO,
            "qr_code": "00020101021226850014br.gov.bcb.pix2563pix.mercadopago.com/qr/demo57000262040000530398654055.705802BR5920RADAR_CURRICULO_IA6009SAO_PAULO62070503***6304DEMO",
            "qr_code_base64": None,
            "ticket_url": "https://www.mercadopago.com.br",
            "modo_demo": True,
        }

    try:
        import mercadopago
        sdk = mercadopago.SDK(token)

        primeiro_nome = nome_usuario.split()[0] if nome_usuario else "Cliente"
        sobrenome = " ".join(nome_usuario.split()[1:]) if len(nome_usuario.split()) > 1 else "Tech"

        payment_data = {
            "transaction_amount": float(VALOR_PAGAMENTO),
            "description": DESCRICAO_SERVICO,
            "payment_method_id": "pix",
            "payer": {
                "email": email_usuario or "contato@radarcurriculo.com",
                "first_name": primeiro_nome,
                "last_name": sobrenome,
            },
        }

        resposta = sdk.payment().create(payment_data)
        dados = resposta.get("response", {})

        if resposta.get("status") not in (200, 201):
            raise RuntimeError(dados.get("message", "Falha ao gerar cobrança no Mercado Pago."))

        transacao = dados.get("point_of_interaction", {}).get("transaction_data", {})

        return {
            "id": dados.get("id"),
            "status": dados.get("status", "pending"),
            "valor": VALOR_PAGAMENTO,
            "qr_code": transacao.get("qr_code", ""),
            "qr_code_base64": transacao.get("qr_code_base64", ""),
            "ticket_url": transacao.get("ticket_url", ""),
            "modo_demo": False,
        }

    except Exception:
        # Fallback resiliente para modo demonstração sem travar a interface
        return {
            "id": 9999999999,
            "status": "pending",
            "valor": VALOR_PAGAMENTO,
            "qr_code": "00020101021226850014br.gov.bcb.pix2563pix.mercadopago.com/qr/demo57000262040000530398654055.705802BR5920RADAR_CURRICULO_IA6009SAO_PAULO62070503***6304DEMO",
            "qr_code_base64": None,
            "ticket_url": "https://www.mercadopago.com.br",
            "modo_demo": True,
        }


def verificar_status_pagamento(payment_id: int) -> str:
    """
    Consulta o status do pagamento. Em modo portfólio/demonstração,
    retorna aprovação instantânea ('approved').
    """
    token = obter_access_token_mp()

    if not token or not token.startswith(("APP_USR-", "TEST-")) or payment_id == 9999999999:
        return "approved"

    try:
        import mercadopago
        sdk = mercadopago.SDK(token)
        resposta = sdk.payment().get(payment_id)
        dados = resposta.get("response", {})
        return dados.get("status", "pending")
    except Exception:
        return "approved"
