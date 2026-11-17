"""
Testes Unitários Automatizados - Radar Currículo IA
Valida os módulos de extração de texto, inteligência semântica,
checkout Pix, autenticação e utilitários do Web Scraper.
"""

import os
import sys
from pathlib import Path

# Garante que a raiz do repositório esteja no sys.path para importação de modules
RAIZ_REPOSITORIO = Path(__file__).resolve().parent.parent
if str(RAIZ_REPOSITORIO) not in sys.path:
    sys.path.insert(0, str(RAIZ_REPOSITORIO))

from modules.leitor_ia import extrair_palavras_chave, extrair_texto_pdf
from modules.pagamento_mp import (
    VALOR_PAGAMENTO,
    criar_pagamento_pix,
    verificar_status_pagamento,
)
from modules.auth_google import is_google_configurado, gerar_url_login_google
from modules.scraper_publico import detectar_modelo_trabalho, limpar_localidade


def test_leitor_ia_palavras_chave():
    """Valida a extração de habilidades no modo simulação."""
    habilidades = extrair_palavras_chave("Currículo de Desenvolvedor Python e Streamlit", delay_segundos=0)
    assert isinstance(habilidades, str)
    assert len(habilidades) > 0
    assert "Python" in habilidades or "Automação" in habilidades or "Streamlit" in habilidades


def test_leitor_ia_pdf_exemplo():
    """Valida se o leitor de PDF lê corretamente o arquivo de teste."""
    caminho_pdf = Path(__file__).resolve().parent.parent / "samples" / "curriculo_exemplo.pdf"
    if caminho_pdf.exists():
        with open(caminho_pdf, "rb") as f:
            texto = extrair_texto_pdf(f)
            assert isinstance(texto, str)
            assert len(texto) > 0


def test_pagamento_mp_pix():
    """Valida a geração de cobrança Pix mock."""
    cobranca = criar_pagamento_pix(
        email_usuario="teste@exemplo.com",
        nome_usuario="Dev Candidato",
    )
    assert cobranca is not None
    assert "id" in cobranca
    assert "qr_code" in cobranca
    assert cobranca["status"] == "pending"


def test_pagamento_mp_status():
    """Valida a consulta de status de pagamento."""
    status = verificar_status_pagamento("mock_pix_12345")
    assert status in ["pending", "approved", "simulado_aprovado"]


def test_auth_google():
    """Valida os utilitários de autenticação Google."""
    configurado = is_google_configurado()
    assert isinstance(configurado, bool)

    url_login = gerar_url_login_google()
    assert isinstance(url_login, str)
    assert "accounts.google.com" in url_login


def test_scraper_detectar_modelo():
    """Valida a classificação inteligente do modelo de trabalho."""
    assert detectar_modelo_trabalho("Vaga 100% Home Office", "Dev Python", "Brasil") == "Remoto"
    assert detectar_modelo_trabalho("Modelo Híbrido 2x presencial", "Dev", "São Paulo (Híbrido)") == "Híbrido"
    assert detectar_modelo_trabalho("Trabalho on-site em escritório", "Analista", "Campinas") == "Presencial"


def test_scraper_limpar_localidade():
    """Valida a remoção de rótulos de modelo do campo de localidade."""
    loc_suja = "São Paulo, SP (Híbrido)"
    loc_limpa = limpar_localidade(loc_suja)
    assert loc_limpa == "São Paulo, SP"


if __name__ == "__main__":
    print("Executando testes unitários...")
    test_leitor_ia_palavras_chave()
    test_leitor_ia_pdf_exemplo()
    test_pagamento_mp_pix()
    test_pagamento_mp_status()
    test_auth_google()
    test_scraper_detectar_modelo()
    test_scraper_limpar_localidade()
    print("✅ Todos os testes unitários passaram com sucesso!")
