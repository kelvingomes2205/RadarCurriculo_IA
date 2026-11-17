"""
Módulo leitor_ia.py
Responsável pela extração de texto de currículos em PDF (via PyPDF2)
e motor de inteligência semântica em Modo Simulação (Mock), garantindo
execução 100% segura, gratuita e sem consumo de APIs externas ou cartões de crédito.
"""

import io
import time
from typing import Union, BinaryIO


def extrair_texto_pdf(arquivo_pdf: Union[str, BinaryIO, io.BytesIO]) -> str:
    """
    Extrai o conteúdo de texto de um arquivo PDF utilizando PyPDF2.

    Args:
        arquivo_pdf: Arquivo PDF ou buffer de bytes do Streamlit.

    Returns:
        str: Texto completo extraído do currículo.
    """
    try:
        from PyPDF2 import PdfReader

        reader = PdfReader(arquivo_pdf)
        texto_completo = []

        for pagina in reader.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo.append(texto_pagina.strip())

        texto_final = "\n".join(texto_completo).strip()

        if not texto_final:
            raise ValueError(
                "Não foi possível extrair texto legível do PDF. Certifique-se de que o documento "
                "não é apenas uma imagem digitalizada."
            )

        return texto_final

    except Exception as e:
        if isinstance(e, ValueError):
            raise e
        raise RuntimeError(f"Erro ao processar o arquivo PDF: {str(e)}") from e


def extrair_palavras_chave(texto_curriculo: str, delay_segundos: float = 3.5) -> str:
    """
    Simula a análise semântica de IA generativa com atraso artificial (3 a 5 segundos)
    e retorna palavras-chave de TI de alto impacto para varredura de vagas.

    Modo Mock (Portfólio / Demonstração Segura):
    - Zero consumo de tokens ou custos financeiros.
    - Analisa o texto do documento e entrega termos perfeitamente alinhados ao mercado.

    Args:
        texto_curriculo: Conteúdo textual do currículo extraído do PDF.
        delay_segundos: Tempo de processamento simulado (padrão: 3.5s).

    Returns:
        str: Palavras-chave separadas por espaço ideais para busca no LinkedIn.
    """
    # Atraso realista de processamento do modelo generativo
    tempo_espera = max(3.0, min(delay_segundos, 5.0))
    time.sleep(tempo_espera)

    if not texto_curriculo or not texto_curriculo.strip():
        return "Python Streamlit Automação"

    texto_lower = texto_curriculo.lower()

    # Mapeamento semântico inteligente de competências baseado no conteúdo
    if "dados" in texto_lower or "power bi" in texto_lower or "pandas" in texto_lower:
        return "Python SQL Dados"
    elif "react" in texto_lower or "frontend" in texto_lower or "javascript" in texto_lower:
        return "React JavaScript Frontend"
    elif "java" in texto_lower and "spring" in texto_lower:
        return "Java Spring Boot"
    else:
        # Padrão de destaque do portfólio
        return "Python Streamlit Automação"
