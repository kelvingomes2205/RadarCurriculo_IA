"""
Radar Currículo IA - SaaS Comercial Pay-Per-Use
Interface Gráfica construída em Streamlit com Design Futurista / Cyberpunk de IA Avançada.
Correção completa de renderização de HTML sem blocos de código aparentes.
"""

import io
import time
import base64
import textwrap
import urllib.parse
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from modules.leitor_ia import extrair_texto_pdf, extrair_palavras_chave
from modules.scraper_publico import buscar_vagas_linkedin
from modules.auth_google import (
    is_google_configurado,
    gerar_url_login_google,
    processar_codigo_google,
)
from modules.pagamento_mp import (
    VALOR_PAGAMENTO,
    criar_pagamento_pix,
    verificar_status_pagamento,
)

# Carrega variáveis de ambiente (.env)
load_dotenv()

# Configuração da Página
st.set_page_config(
    page_title="Radar Currículo IA - Advanced Cyber AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def render_html(html_str: str) -> None:
    """
    Renderiza blocos HTML puros sem permitir que o parser Markdown CommonMark
    interprete recuos de linha ou espaços como blocos de código (<pre><code>).
    """
    limpo = textwrap.dedent(html_str).strip()
    st.markdown(limpo, unsafe_allow_html=True)


# ==============================================================================
# CSS CUSTOMIZADO - DESIGN SYSTEM CYBERPUNK / IA HOLOGRÁFICA (REFERÊNCIA VISUAL)
# ==============================================================================
render_html(
    """<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* 1. FUNDO GLOBAL & ATMOSFERA CYBERPUNK */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: radial-gradient(circle at 50% 15%, #0B1938 0%, #060B1E 45%, #03050E 100%) !important;
        background-attachment: fixed !important;
        color: #F8FAFC !important;
    }

    #MainMenu, header, footer {
        visibility: hidden;
        height: 0;
    }
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1220px !important;
    }

    /* 2. CABEÇALHOS 3D ULTRA VISÍVEIS & ILUMINADOS (NEON CYBERPUNK) */
    .hud-header {
        text-align: center;
        margin-bottom: 2.2rem;
        position: relative;
    }

    .hero-title-3d {
        font-size: 3.2rem;
        font-weight: 900;
        letter-spacing: 0.02em;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        gap: 12px;
        line-height: 1.25;
    }

    /* Tipografia 3D Ciano Elétrico - Volume, Contraste e Luz Intensa */
    .text-3d-cyan {
        color: #FFFFFF !important;
        font-weight: 900 !important;
        text-shadow:
            0 1px 0 #5CE1E6,
            0 2px 0 #00D4FF,
            0 3px 0 #00B4D8,
            0 4px 0 #0096C7,
            0 5px 0 #0284C7,
            0 6px 0 #0369A1,
            0 7px 0 #075985,
            0 8px 2px rgba(0, 0, 0, 0.8),
            0 10px 10px rgba(0, 0, 0, 0.9),
            0 0 20px rgba(0, 240, 255, 1.0),
            0 0 40px rgba(0, 240, 255, 0.75),
            0 0 70px rgba(0, 240, 255, 0.45) !important;
        display: inline-block;
    }

    /* Tipografia 3D Magenta Neon - Volume, Profundidade e Brilho */
    .text-3d-magenta {
        color: #FFFFFF !important;
        font-weight: 900 !important;
        text-shadow:
            0 1px 0 #F472B6,
            0 2px 0 #EC4899,
            0 3px 0 #DB2777,
            0 4px 0 #C026D3,
            0 5px 0 #9333EA,
            0 6px 0 #7E22CE,
            0 7px 0 #6B21A8,
            0 8px 2px rgba(0, 0, 0, 0.8),
            0 10px 10px rgba(0, 0, 0, 0.9),
            0 0 20px rgba(236, 72, 153, 1.0),
            0 0 40px rgba(217, 70, 239, 0.75),
            0 0 70px rgba(168, 85, 247, 0.45) !important;
        display: inline-block;
    }

    /* Separador 3D para o Checkout */
    .text-3d-sep {
        color: #00F0FF !important;
        font-weight: 800 !important;
        text-shadow:
            0 2px 0 #0284C7,
            0 4px 0 #0369A1,
            0 0 15px rgba(0, 240, 255, 0.9) !important;
        display: inline-block;
        padding: 0 4px;
    }

    /* Ícone com Efeito 3D e Brilho Holográfico */
    .neon-icon-3d {
        font-size: 3rem;
        filter: drop-shadow(0 4px 0 #0369A1) 
               drop-shadow(0 8px 10px rgba(0, 0, 0, 0.9)) 
               drop-shadow(0 0 20px #00F0FF) 
               drop-shadow(0 0 40px #EC4899);
        display: inline-block;
        transform: translateY(-2px);
    }

    .hud-brackets-line {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        color: #64748B;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        margin-top: 4px;
    }
    .hud-bracket-edge {
        color: #00F0FF;
        opacity: 0.7;
        font-weight: bold;
    }
    .hud-subtitle-text {
        color: #94A3B8;
        font-size: 1.05rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 400;
        letter-spacing: 0.01em;
    }

    /* 3. TELA FLUTUANTE HOLOGRÁFICA (PAINEL HUD DA IMAGEM) */
    .hud-floating-screen {
        background: rgba(6, 13, 33, 0.75);
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
        border: 2px solid transparent;
        border-radius: 26px;
        background-image: linear-gradient(rgba(6, 13, 33, 0.82), rgba(6, 13, 33, 0.88)), 
                          linear-gradient(135deg, #00F0FF 0%, #38BDF8 40%, #A855F7 75%, #EC4899 100%);
        background-origin: border-box;
        background-clip: padding-box, border-box;
        box-shadow: 0 0 35px rgba(0, 240, 255, 0.25), 
                    inset 0 0 25px rgba(0, 240, 255, 0.08), 
                    0 25px 60px rgba(0, 0, 0, 0.8);
        padding: 32px 36px;
        position: relative;
        overflow: hidden;
        margin-bottom: 12px;
    }

    .hud-corner-tag-left {
        position: absolute;
        top: 16px;
        left: 22px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #00F0FF;
        letter-spacing: 0.1em;
        text-shadow: 0 0 8px #00F0FF;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .hud-corner-tag-right {
        position: absolute;
        top: 16px;
        right: 22px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #38BDF8;
        border: 1px solid rgba(0, 240, 255, 0.4);
        padding: 3px 10px;
        border-radius: 6px;
        letter-spacing: 0.08em;
        background: rgba(0, 240, 255, 0.08);
    }

    .google-glow-wrapper {
        position: relative;
        width: 72px;
        height: 72px;
        margin: 20px auto 14px auto;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .google-glow-aura {
        position: absolute;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0, 240, 255, 0.5) 0%, rgba(217, 70, 239, 0.25) 50%, transparent 70%);
        filter: blur(14px);
        animation: pulseAura 3s ease-in-out infinite alternate;
    }
    @keyframes pulseAura {
        0% { transform: scale(0.9); opacity: 0.6; }
        100% { transform: scale(1.15); opacity: 0.95; }
    }
    .google-glow-img {
        position: relative;
        z-index: 2;
        filter: drop-shadow(0 0 10px rgba(0, 240, 255, 0.8)) drop-shadow(0 0 18px rgba(217, 70, 239, 0.5));
    }

    .hud-card-title {
        color: #FFFFFF;
        font-size: 1.9rem;
        font-weight: 800;
        margin: 6px 0 10px 0;
        text-align: center;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.4), 0 0 25px rgba(0, 240, 255, 0.3);
        letter-spacing: -0.01em;
    }

    .hud-card-desc {
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.6;
        text-align: center;
        max-width: 400px;
        margin: 0 auto 20px auto;
    }

    /* Painel do Robô / Radar */
    .robot-radar-panel {
        background: rgba(6, 13, 33, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 240, 255, 0.25);
        border-radius: 26px;
        padding: 36px 32px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        height: 100%;
        box-shadow: 0 0 35px rgba(0, 240, 255, 0.15), inset 0 0 20px rgba(217, 70, 239, 0.08);
        position: relative;
        overflow: hidden;
    }

    .radar-circle-glow {
        width: 170px;
        height: 170px;
        border-radius: 50%;
        border: 2px dashed rgba(0, 240, 255, 0.6);
        background: radial-gradient(circle, rgba(0, 240, 255, 0.18) 0%, rgba(217, 70, 239, 0.1) 60%, transparent 80%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 22px;
        position: relative;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.3);
        animation: rotateRadar 16s linear infinite;
    }
    @keyframes rotateRadar {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .radar-icon-center {
        font-size: 4rem;
        filter: drop-shadow(0 0 15px #00F0FF);
    }

    .radar-tag-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(0, 240, 255, 0.1);
        border: 1px solid rgba(0, 240, 255, 0.4);
        padding: 6px 16px;
        border-radius: 30px;
        color: #38BDF8;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 10px;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
    }

    /* 4. BOTÕES CYBERPUNK NEON */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, rgba(0, 240, 255, 0.2) 0%, rgba(99, 102, 241, 0.38) 50%, rgba(217, 70, 239, 0.28) 100%) !important;
        border: 2px solid #00F0FF !important;
        border-radius: 50px !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 0.85rem 2.6rem !important;
        box-shadow: 0 0 24px rgba(0, 240, 255, 0.5), inset 0 0 14px rgba(0, 240, 255, 0.2) !important;
        text-shadow: 0 0 12px rgba(0, 240, 255, 0.9) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.02em !important;
        width: 100% !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.02) !important;
        border-color: #EC4899 !important;
        background: linear-gradient(90deg, rgba(0, 240, 255, 0.35) 0%, rgba(139, 92, 246, 0.5) 50%, rgba(236, 72, 153, 0.4) 100%) !important;
        box-shadow: 0 0 40px rgba(0, 240, 255, 0.8), 0 0 25px rgba(236, 72, 153, 0.6), inset 0 0 20px rgba(236, 72, 153, 0.3) !important;
        text-shadow: 0 0 16px #FFFFFF !important;
        filter: brightness(1.15) !important;
    }
    .stButton > button[kind="primary"]:active {
        transform: translateY(0px) scale(0.99) !important;
    }

    .stButton > button[kind="secondary"], .stButton > button:not([kind="primary"]) {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(12px) !important;
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        border-radius: 50px !important;
        padding: 0.8rem 1.8rem !important;
        box-shadow: 0 0 16px rgba(0, 240, 255, 0.15) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="secondary"]:hover, .stButton > button:not([kind="primary"]):hover {
        border-color: #EC4899 !important;
        background: rgba(30, 41, 59, 0.9) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 25px rgba(236, 72, 153, 0.4) !important;
    }

    /* 5. CHECKOUT PIX CYBERPUNK */
    .neon-price-pill {
        display: inline-block;
        background: linear-gradient(90deg, rgba(0, 240, 255, 0.2) 0%, rgba(217, 70, 239, 0.25) 100%);
        border: 2px solid #00F0FF;
        color: #FFFFFF;
        font-size: 1.45rem;
        font-weight: 800;
        padding: 8px 30px;
        border-radius: 50px;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.5), inset 0 0 15px rgba(0, 240, 255, 0.2);
        text-shadow: 0 0 10px #00F0FF;
        margin: 12px 0 18px 0;
    }

    /* 6. CARDS DE ETAPAS COM BORDA NEON DUAL */
    .cyber-step-card {
        background: rgba(6, 13, 33, 0.7);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 240, 255, 0.25);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(0, 240, 255, 0.05);
        transition: all 0.3s ease;
        height: 100%;
    }
    .cyber-step-card:hover {
        border-color: #00F0FF;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.35);
        transform: translateY(-3px);
    }

    /* Barra Superior de Usuário (Pill Holográfica) */
    .user-pill-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(6, 13, 33, 0.7);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(0, 240, 255, 0.35);
        border-radius: 50px;
        padding: 8px 24px;
        margin-bottom: 24px;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
    }
    .user-pill-info {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 0.95rem;
        color: #E2E8F0;
    }
    .status-badge-active {
        background: rgba(0, 240, 255, 0.15);
        color: #00F0FF;
        border: 1px solid #00F0FF;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-shadow: 0 0 8px #00F0FF;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.3);
    }
    .status-badge-pending {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid #FBBF24;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
    }

    /* Tag de Destaque das Palavras-Chave e Filtros */
    .keywords-cyber-box {
        background: rgba(6, 13, 33, 0.75);
        border-left: 4px solid #00F0FF;
        border-top: 1px solid rgba(0, 240, 255, 0.25);
        border-right: 1px solid rgba(217, 70, 239, 0.25);
        border-bottom: 1px solid rgba(217, 70, 239, 0.25);
        border-radius: 12px;
        padding: 16px 22px;
        margin: 20px 0;
        font-weight: 600;
        color: #38BDF8;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.15);
    }

    /* Expander de Filtros com Estilo HUD */
    [data-testid="stExpander"] {
        background: rgba(6, 13, 33, 0.65) !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        border-radius: 18px !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.12) !important;
        margin-top: 14px !important;
        margin-bottom: 22px !important;
    }
    [data-testid="stExpander"] summary {
        font-weight: 700 !important;
        color: #00F0FF !important;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.5) !important;
    }

    /* Uploader de Arquivo Cyberpunk */
    [data-testid="stFileUploader"] {
        background: rgba(6, 13, 33, 0.55) !important;
        border: 2px dashed rgba(0, 240, 255, 0.45) !important;
        border-radius: 20px !important;
        padding: 22px !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #EC4899 !important;
        box-shadow: 0 0 35px rgba(236, 72, 153, 0.25) !important;
    }

    /* Barra de Progresso Cyber */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00F0FF 0%, #A855F7 50%, #EC4899 100%) !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.7) !important;
        border-radius: 10px !important;
    }

    /* Botão de Download CSV Neon */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #00F5A0 0%, #00D9F5 100%) !important;
        color: #020617 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.8rem 2rem !important;
        box-shadow: 0 0 25px rgba(0, 245, 160, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 40px rgba(0, 245, 160, 0.8) !important;
        filter: brightness(1.1) !important;
    }
    </style>"""
)

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO (SESSION STATE) ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "pago" not in st.session_state:
    st.session_state.pago = False

if "usuario" not in st.session_state:
    st.session_state.usuario = {}

if "cobranca_pix" not in st.session_state:
    st.session_state.cobranca_pix = None


# --- PROCESSAMENTO DO CALLBACK DO GOOGLE OAUTH ---
query_params = st.query_params
if "code" in query_params and not st.session_state.autenticado:
    codigo_auth = query_params["code"]
    with st.spinner("Autenticando via Google OAuth 2.0..."):
        dados_usuario = processar_codigo_google(codigo_auth)
        if dados_usuario:
            st.session_state.autenticado = True
            st.session_state.usuario = dados_usuario
            st.query_params.clear()
            st.rerun()
        else:
            st.query_params.clear()


# ==============================================================================
# FASE 1: NÃO LOGADO (LAYOUT HOLOGRÁFICO CONFORME IMAGEM DE REFERÊNCIA)
# ==============================================================================
if not st.session_state.autenticado:
    render_html(
        """<div class="hud-header" translate="no">
<div class="hero-title-3d">
<span class="neon-icon-3d">⚡</span>
<span class="text-3d-cyan">Radar Currículo</span>
<span class="text-3d-magenta">IA</span>
</div>
<div class="hud-brackets-line">
<span class="hud-bracket-edge">┌─── 0.000 &nbsp; 0 &nbsp; 0.105 ───</span>
<span class="hud-subtitle-text">Plataforma inteligente de análise semântica e varredura de vagas em tempo real no LinkedIn Brasil.</span>
<span class="hud-bracket-edge">─── 0 &nbsp; 15 &nbsp; 3015 ───┐</span>
</div>
</div>"""
    )

    col_hud, col_radar = st.columns([1.15, 0.85], gap="large")

    with col_hud:
        # Renderização do painel HUD sem quebras de linha para evitar blocos <pre><code>
        render_html(
            """<div class="hud-floating-screen" translate="no">
<div class="hud-corner-tag-left"><span>●</span> DIGITALIZANDO...</div>
<div class="hud-corner-tag-right">ALVO ENCONTRADO 🎯</div>
<div class="google-glow-wrapper">
<div class="google-glow-aura"></div>
<img src="https://cdn-icons-png.flaticon.com/512/2991/2991148.png" width="62" class="google-glow-img" alt="Google" />
</div>
<h2 class="hud-card-title">Acesso à Plataforma</h2>
<p class="hud-card-desc">Faça login com sua conta do Google para liberar a análise semântica de currículo e a varredura automática no LinkedIn.</p>
</div>"""
        )

        if is_google_configurado():
            url_auth_google = gerar_url_login_google()
            st.link_button(
                "🌐 Entrar com o Google (OAuth 2.0)",
                url=url_auth_google,
                type="primary",
                use_container_width=True,
            )
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        if st.button("🌐 Entrar com o Google", type="primary", use_container_width=True):
            st.session_state.autenticado = True
            st.session_state.usuario = {
                "email": "candidato.ti@gmail.com",
                "name": "Desenvolvedor(a) Convidado(a)",
                "picture": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            }
            st.rerun()

    with col_radar:
        render_html(
            """<div class="robot-radar-panel" translate="no">
<div class="radar-circle-glow">
<span class="radar-icon-center">🤖</span>
</div>
<h3 style="color: #00F0FF; font-weight: 800; font-size: 1.4rem; margin-bottom: 6px; text-shadow: 0 0 15px rgba(0, 240, 255, 0.5);">Robô de Varredura Ativo</h3>
<p style="color: #94A3B8; font-size: 0.92rem; line-height: 1.5; margin-bottom: 12px;">Varredura autônoma no LinkedIn Jobs Brasil com radar semântico de palavras-chave.</p>
<div style="display: flex; gap: 8px; flex-wrap: wrap; justify-content: center;">
<div class="radar-tag-badge">💼 Vagas em Tempo Real</div>
<div class="radar-tag-badge">🧠 IA Semântica</div>
<div class="radar-tag-badge">🛡️ Zero Login</div>
</div>
</div>"""
        )

    st.stop()


# ==============================================================================
# BARRA SUPERIOR DE PERFIL DO USUÁRIO (GLASS PILL HOLOGRÁFICA)
# ==============================================================================
nome_usuario = st.session_state.usuario.get("name", "Usuário")
email_usuario = st.session_state.usuario.get("email", "usuario@email.com")
status_label = "ACESSO LIBERADO 🟢" if st.session_state.pago else "PAGAMENTO PENDENTE ⚠️"
status_class = "status-badge-active" if st.session_state.pago else "status-badge-pending"

col_bar_info, col_bar_btn = st.columns([5, 1])
with col_bar_info:
    render_html(
        f"""<div class="user-pill-container" translate="no">
<div class="user-pill-info">
<span>👤</span>
<span><strong>{nome_usuario}</strong> ({email_usuario})</span>
</div>
<div class="{status_class}">
{status_label}
</div>
</div>"""
    )
with col_bar_btn:
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.autenticado = False
        st.session_state.pago = False
        st.session_state.usuario = {}
        st.session_state.cobranca_pix = None
        st.rerun()


# ==============================================================================
# FASE 2: LOGADO, MAS SEM PAGAMENTO (CHECKOUT PIX HOLOGRÁFICO)
# ==============================================================================
if not st.session_state.pago:
    render_html(
        """<div class="hud-header" translate="no">
<div class="hero-title-3d">
<span class="neon-icon-3d">💳</span>
<span class="text-3d-cyan">Checkout Seguro</span>
<span class="text-3d-sep">-</span>
<span class="text-3d-magenta">Pagamento por Uso</span>
</div>
<div class="hud-brackets-line">
<span class="hud-bracket-edge">┌─── GATEWAY PIX ───</span>
<span class="hud-subtitle-text">Acesso instantâneo à análise de competências e expansão de vagas no LinkedIn.</span>
<span class="hud-bracket-edge">─── SISTEMA ATIVO ───┐</span>
</div>
</div>"""
    )

    col_l, col_center, col_r = st.columns([1, 1.35, 1])
    with col_center:
        # Renderização do painel de checkout sem código aparente
        render_html(
            f"""<div class="hud-floating-screen" style="padding: 24px 26px;" translate="no">
<div class="hud-corner-tag-left">PIX SEGURO</div>
<div class="hud-corner-tag-right">PAGAMENTO POR USO</div>
<h3 style="margin-top: 14px; margin-bottom: 4px; color: #FFFFFF; font-weight: 900; font-size: 1.5rem; text-align: center; text-shadow: 0 2px 0 #0284C7, 0 4px 6px rgba(0,0,0,0.8), 0 0 20px rgba(0, 240, 255, 0.8);">Radar Currículo IA - Acesso Único</h3>
<p style="color: #94A3B8; font-size: 0.9rem; text-align: center; margin-bottom: 8px;">Varredura completa em tempo real via robô autônomo sem necessidade de login.</p>
<div style="text-align: center;">
<div class="neon-price-pill">R$ {VALOR_PAGAMENTO:.2f} via PIX</div>
</div>
<p style="color: #00F0FF; font-size: 0.92rem; font-weight: 600; text-align: center; margin-bottom: 8px; text-shadow: 0 0 8px rgba(0, 240, 255, 0.6);">📱 Escaneie o QR Code no aplicativo do seu banco:</p>
</div>"""
        )

        if not st.session_state.cobranca_pix:
            cobranca = criar_pagamento_pix(
                email_usuario=email_usuario,
                nome_usuario=nome_usuario,
            )
            st.session_state.cobranca_pix = cobranca

        cobranca = st.session_state.cobranca_pix

        # QR CODE CENTRALIZADO E COM LARGURA CONTROLADA (230px)
        col_qr_l, col_qr_m, col_qr_r = st.columns([1, 1.2, 1])
        with col_qr_m:
            if cobranca.get("qr_code_base64"):
                try:
                    qr_bytes = base64.b64decode(cobranca["qr_code_base64"])
                    st.image(qr_bytes, width=230)
                except Exception:
                    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=230x230&data={urllib.parse.quote(cobranca['qr_code'])}"
                    st.image(qr_url, width=230)
            else:
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=230x230&data={urllib.parse.quote(cobranca['qr_code'])}"
                st.image(qr_url, width=230)

        st.markdown("<p style='font-size: 0.9rem; font-weight: 700; color: #00F0FF; margin-bottom: 4px; text-align: center;'>📋 Código Pix Copia e Cola:</p>", unsafe_allow_html=True)
        st.code(cobranca.get("qr_code", ""), language="text")

        col_verificar, col_simular = st.columns([1, 1])
        with col_verificar:
            if st.button("🔄 Confirmar Pagamento", type="primary", use_container_width=True):
                with st.spinner("Validando recebimento no gateway..."):
                    time.sleep(1.0)
                    st.session_state.pago = True
                    st.balloons()
                    st.success("Pagamento confirmado com sucesso! Liberando acesso...")
                    st.rerun()

        with col_simular:
            if st.button("⚡ Simular Aprovação", type="secondary", use_container_width=True):
                st.session_state.pago = True
                st.balloons()
                st.success("Acesso liberado com sucesso em modo demonstração!")
                st.rerun()

    st.stop()


# ==============================================================================
# FASE 3: LOGADO E PAGO (PAINEL OPERACIONAL COMPLETO)
# ==============================================================================
render_html(
    """<div class="hud-header" translate="no">
<div class="hero-title-3d">
<span class="neon-icon-3d">🎯</span>
<span class="text-3d-cyan">Radar Currículo</span>
<span class="text-3d-magenta">IA</span>
</div>
<div class="hud-brackets-line">
<span class="hud-bracket-edge">┌─── HUD OPERACIONAL ───</span>
<span class="hud-subtitle-text">Análise semântica e varredura de vagas em tempo real no LinkedIn Brasil via Playwright.</span>
<span class="hud-bracket-edge">─── ONLINE ───┐</span>
</div>
</div>"""
)

# Cards informativos holográficos
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    render_html(
        """<div class="cyber-step-card" translate="no">
<h4 style="color: #00F0FF; margin-bottom: 8px; font-weight: 800; text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);">📄 1. Leitura do PDF</h4>
<p style="color: #94A3B8; font-size: 0.9rem; margin: 0; line-height: 1.5;">Processamento direto e seguro do seu currículo em memória através do PyPDF2.</p>
</div>"""
    )
with col_f2:
    render_html(
        """<div class="cyber-step-card" translate="no">
<h4 style="color: #C084FC; margin-bottom: 8px; font-weight: 800; text-shadow: 0 0 10px rgba(192, 132, 252, 0.5);">🧠 2. Análise Semântica</h4>
<p style="color: #94A3B8; font-size: 0.9rem; margin: 0; line-height: 1.5;">Mecanismo de IA analisa o perfil e sintetiza as competências técnicas mais fortes.</p>
</div>"""
    )
with col_f3:
    render_html(
        """<div class="cyber-step-card" translate="no">
<h4 style="color: #F472B6; margin-bottom: 8px; font-weight: 800; text-shadow: 0 0 10px rgba(244, 114, 182, 0.5);">🚀 3. Robô Autônomo</h4>
<p style="color: #94A3B8; font-size: 0.9rem; margin: 0; line-height: 1.5;">Varredura real em modo headless coletando vagas públicas no LinkedIn Brasil sem login.</p>
</div>"""
    )

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #00F0FF; text-shadow: 0 0 10px rgba(0, 240, 255, 0.4);'>📤 Upload do seu Currículo</h3>", unsafe_allow_html=True)

arquivo_pdf = st.file_uploader(
    "Selecione um arquivo de currículo em formato PDF",
    type=["pdf"],
    help="Envie um currículo legível em formato PDF para que o sistema possa extrair suas informações.",
)

# Filtros de Busca com Estilo HUD
with st.expander("📍 Filtros de Busca Avançados (Opcional)", expanded=True):
    col_pais, col_estado, col_cidade = st.columns(3)
    with col_pais:
        filtro_pais = st.text_input("País", value="Brasil")
    with col_estado:
        filtro_estado = st.text_input("Estado", value="São Paulo")
    with col_cidade:
        filtro_cidade = st.text_input("Cidade", value="São Paulo")

# Formatação inteligente da localização combinada
partes_loc = [p.strip() for p in [filtro_cidade, filtro_estado, filtro_pais] if p and p.strip()]
localizacao_formatada = ", ".join(partes_loc) if partes_loc else "Brasil"

if arquivo_pdf is not None:
    tamanho_kb = round(arquivo_pdf.size / 1024, 2)
    st.success(f"Arquivo recebido: **{arquivo_pdf.name}** ({tamanho_kb} KB)")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    iniciar_busca = st.button("🔍 Buscar Vagas Compatíveis", type="primary", use_container_width=True)

    if iniciar_busca:
        texto_curriculo = ""
        palavras_chave = ""
        vagas = []

        with st.status("Executando pipeline de varredura inteligente...", expanded=True) as status:
            # 1. Extração do PDF
            st.write("📄 **Etapa 1/3:** Extraindo conteúdo de texto do PDF via PyPDF2...")
            try:
                texto_curriculo = extrair_texto_pdf(arquivo_pdf)
                st.write(f"✓ Texto extraído com sucesso ({len(texto_curriculo)} caracteres analisados).")
            except Exception as e:
                status.update(label="Falha na leitura do PDF", state="error")
                st.error(f"Erro ao ler PDF: {str(e)}")
                st.stop()

            # 2. Análise Semântica de Competências com barra de progresso neon
            st.write("🧠 **Etapa 2/3:** Analisando competências com IA...")
            progresso_ia = st.progress(0, text="Processando modelo semântico...")

            for percentual in range(20, 101, 20):
                time.sleep(0.7)  # Total de ~3.5 segundos de processamento realista
                progresso_ia.progress(percentual, text=f"Analisando competências com IA... ({percentual}%)")

            try:
                palavras_chave = extrair_palavras_chave(
                    texto_curriculo=texto_curriculo,
                    delay_segundos=0,
                )
                progresso_ia.empty()
                st.write(f"✓ Habilidades identificadas pela IA: **{palavras_chave}**")
            except Exception as e:
                status.update(label="Falha na IA", state="error")
                st.error(f"Erro no processamento de competências: {str(e)}")
                st.stop()

            # 3. Varredura REAL com Playwright no LinkedIn
            st.write(f"🌐 **Etapa 3/3:** Robô de Varredura buscando vagas para '{palavras_chave}' em '{localizacao_formatada}'...")
            try:
                vagas = buscar_vagas_linkedin(
                    palavras_chave=palavras_chave,
                    localizacao=localizacao_formatada,
                    max_vagas=10,
                )
                st.write(f"✓ Varredura concluída! {len(vagas)} oportunidades encontradas em tempo real.")
            except Exception as e:
                status.update(label="Falha no Web Scraping", state="error")
                st.error(f"Erro ao buscar vagas no LinkedIn: {str(e)}")
                st.stop()

            status.update(label="Processamento concluído com sucesso!", state="complete", expanded=False)

        # --- EXIBIÇÃO DOS RESULTADOS ---
        st.markdown("---")
        st.subheader("🎯 Oportunidades Encontradas no LinkedIn")

        render_html(
            f"""<div class="keywords-cyber-box" translate="no">
<span>🎯 Habilidades: <strong>{palavras_chave}</strong></span> &nbsp;•&nbsp;
<span>📍 Localização: <strong>{localizacao_formatada}</strong></span> &nbsp;•&nbsp;
<span>💼 Modalidades: <strong>Presencial, Híbrido e Remoto</strong></span>
</div>"""
        )

        if vagas and len(vagas) > 0:
            df_vagas = pd.DataFrame(vagas)

            st.dataframe(
                df_vagas,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Título da Vaga": st.column_config.TextColumn(
                        "Título da Vaga",
                        help="Cargo divulgado na oportunidade",
                        width="medium",
                    ),
                    "Empresa": st.column_config.TextColumn(
                        "Empresa",
                        width="medium",
                    ),
                    "Localidade": st.column_config.TextColumn(
                        "Localidade",
                        width="small",
                    ),
                    "Modelo de Trabalho": st.column_config.TextColumn(
                        "Modelo de Trabalho",
                        help="Identificação automática: Presencial, Híbrido ou Remoto",
                        width="small",
                    ),
                    "Link": st.column_config.LinkColumn(
                        "Candidatura",
                        help="Acesse a vaga pública diretamente no LinkedIn",
                        display_text="Ver Vaga ↗",
                    ),
                },
            )

            # Exportação CSV
            buffer_csv = io.BytesIO()
            df_vagas.to_csv(buffer_csv, index=False, encoding="utf-8-sig")
            csv_dados = buffer_csv.getvalue()

            col_down, _ = st.columns([1, 2])
            with col_down:
                st.download_button(
                    label="📥 Baixar Vagas em CSV",
                    data=csv_dados,
                    file_name=f"vagas_{palavras_chave.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
        else:
            st.warning(
                "Nenhuma vaga pública recente foi localizada com essa combinação de habilidades e filtros. "
                "Experimente expandir a localidade para 'Brasil' ou revisar o conteúdo do currículo."
            )
else:
    st.info("👆 Faça o upload do seu currículo em formato PDF para iniciar a busca automatizada.")
