"""
Módulo auth_google.py
Gerencia a autenticação com o Google OAuth 2.0 no ecossistema Streamlit.
"""

import os
import urllib.parse
from typing import Optional, Dict
import requests
from dotenv import load_dotenv

load_dotenv()


def obter_credenciais_google() -> Dict[str, str]:
    """
    Recupera as credenciais do Google OAuth a partir de variáveis de ambiente.
    """
    client_id = os.getenv("GOOGLE_CLIENT_ID", "").strip()
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "").strip()
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8501").strip()

    # Fallback para st.secrets caso disponível
    if not client_id:
        try:
            import streamlit as st
            if "GOOGLE_CLIENT_ID" in st.secrets:
                client_id = st.secrets["GOOGLE_CLIENT_ID"]
                client_secret = st.secrets.get("GOOGLE_CLIENT_SECRET", "")
                redirect_uri = st.secrets.get("GOOGLE_REDIRECT_URI", "http://localhost:8501")
        except Exception:
            pass

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }


def is_google_configurado() -> bool:
    """
    Verifica se o client_id e client_secret do Google estão presentes.
    """
    creds = obter_credenciais_google()
    return bool(creds["client_id"] and creds["client_secret"])


def gerar_url_login_google() -> str:
    """
    Gera a URL de autorização oficial do Google OAuth 2.0.
    """
    creds = obter_credenciais_google()
    params = {
        "client_id": creds["client_id"],
        "redirect_uri": creds["redirect_uri"],
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"


def processar_codigo_google(code: str) -> Optional[Dict[str, str]]:
    """
    Troca o authorization code retornado pelo Google por tokens e
    coleta as informações de perfil do usuário (nome, e-mail, foto).
    """
    creds = obter_credenciais_google()
    token_url = "https://oauth2.googleapis.com/token"

    payload = {
        "code": code,
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "redirect_uri": creds["redirect_uri"],
        "grant_type": "authorization_code",
    }

    try:
        token_resp = requests.post(token_url, data=payload, timeout=10)
        if token_resp.status_code != 200:
            return None

        token_data = token_resp.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return None

        userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        user_resp = requests.get(
            userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )

        if user_resp.status_code != 200:
            return None

        user_data = user_resp.json()
        return {
            "email": user_data.get("email", ""),
            "name": user_data.get("name", "Usuário"),
            "picture": user_data.get("picture", ""),
            "id": user_data.get("id", ""),
        }

    except Exception:
        return None
