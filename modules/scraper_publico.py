"""
Módulo scraper_publico.py
Responsável pela busca pública e automatizada de vagas de emprego no LinkedIn
utilizando Playwright em modo Headless, sem necessidade de autenticação/login.
Coleta Título da Vaga, Empresa, Localidade, Modelo de Trabalho (Presencial/Híbrido/Remoto) e Link.
"""

import re
import time
import urllib.parse
from typing import List, Dict
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def detectar_modelo_trabalho(card_texto: str, titulo: str, localidade: str) -> str:
    """
    Detecta de forma inteligente se a vaga é Remota, Híbrida ou Presencial
    analisando os metadados do cartão, o título e a localidade retornada pelo LinkedIn.
    """
    texto_combinado = f"{titulo} {localidade} {card_texto}".lower()

    if any(termo in texto_combinado for termo in ["híbrido", "hibrido", "hybrid"]):
        return "Híbrido"
    elif any(termo in texto_combinado for termo in ["remoto", "remote", "home office", "homeoffice", "teletrabalho"]):
        return "Remoto"
    elif any(termo in texto_combinado for termo in ["presencial", "on-site", "onsite"]):
        return "Presencial"
    else:
        return "Presencial"


def limpar_localidade(localidade_texto: str) -> str:
    """
    Remove tags de modelo entre parênteses da string de localidade para manter o campo limpo.
    Ex: 'São Paulo, SP (Híbrido)' -> 'São Paulo, SP'.
    """
    if not localidade_texto:
        return ""
    limpa = re.sub(
        r"\s*\((Híbrido|Hibrido|Remoto|Presencial|Hybrid|Remote|On-site|Onsite)\)",
        "",
        localidade_texto,
        flags=re.IGNORECASE,
    ).strip()
    return limpa if limpa else localidade_texto


def buscar_vagas_linkedin(
    palavras_chave: str,
    localizacao: str = "Brasil",
    modelo_trabalho: str = "Qualquer",
    max_vagas: int = 10,
) -> List[Dict[str, str]]:
    """
    Realiza uma raspagem pública das vagas mais recentes no LinkedIn Brasil
    correspondentes às palavras-chave e localização fornecidas, trazendo todas
    as modalidades de trabalho e identificando o modelo de cada vaga.

    Args:
        palavras_chave: Habilidades ou cargos alvo para pesquisar.
        localizacao: Localização geográfica (ex: "São Paulo, São Paulo, Brasil").
        modelo_trabalho: Mantido por compatibilidade ("Qualquer" traz todas as modalidades).
        max_vagas: Quantidade máxima de vagas a retornar (padrão: 10).

    Returns:
        List[Dict[str, str]]: Lista contendo dicionários com Título da Vaga,
                              Empresa, Localidade, Modelo de Trabalho e Link de candidatura.
    """
    if not palavras_chave or not palavras_chave.strip():
        return []

    # Codifica as palavras-chave e localização para o formato de query string
    termo_busca = urllib.parse.quote_plus(palavras_chave.strip())
    loc_formatada = localizacao.strip() if localizacao and localizacao.strip() else "Brasil"
    loc_busca = urllib.parse.quote_plus(loc_formatada)

    # URL pública base do LinkedIn com filtro f_TPR=r604800 (última semana / 7 dias)
    url = f"https://br.linkedin.com/jobs/search?keywords={termo_busca}&location={loc_busca}&f_TPR=r604800"

    # Se um modelo específico for passado e não for "Qualquer", aplica o filtro opcional da URL
    mapa_modelo = {
        "Presencial": "1",
        "Remoto": "2",
        "Híbrido": "3",
        "Hibrido": "3",
    }
    if modelo_trabalho in mapa_modelo:
        url += f"&f_WT={mapa_modelo[modelo_trabalho]}"

    vagas_encontradas: List[Dict[str, str]] = []

    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        context = browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1280, "height": 800},
            locale="pt-BR",
            extra_http_headers={
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            },
        )

        page = context.new_page()

        try:
            # Navega até a página de busca pública
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(2.5)  # Pausa estratégica para contornar verificações leves

            # Scroll suave para baixo para carregar os cartões de vagas
            page.evaluate("window.scrollBy(0, 700)")
            time.sleep(1.5)

            # Seletores para os cartões de vagas no LinkedIn público
            seletores_cards = [
                "ul.jobs-search__results-list > li",
                "div.job-search-card",
                "li.job-search-card",
                ".base-card",
            ]

            cards = []
            for seletor in seletores_cards:
                cards = page.query_selector_all(seletor)
                if len(cards) >= 1:
                    break

            for card in cards:
                if len(vagas_encontradas) >= max_vagas:
                    break

                try:
                    # Título da Vaga
                    titulo_elem = (
                        card.query_selector("h3.base-search-card__title")
                        or card.query_selector(".base-search-card__title")
                        or card.query_selector("h3")
                    )
                    titulo = titulo_elem.inner_text().strip() if titulo_elem else "Título não informado"

                    # Empresa
                    empresa_elem = (
                        card.query_selector("h4.base-search-card__subtitle a")
                        or card.query_selector("h4.base-search-card__subtitle")
                        or card.query_selector("a.hidden-nested-link")
                        or card.query_selector(".base-search-card__subtitle")
                    )
                    empresa = empresa_elem.inner_text().strip() if empresa_elem else "Empresa confidencial"

                    # Localidade Bruta
                    local_elem = (
                        card.query_selector("span.job-search-card__location")
                        or card.query_selector(".job-search-card__location")
                        or card.query_selector(".base-search-card__metadata")
                    )
                    localidade_bruta = local_elem.inner_text().strip() if local_elem else loc_formatada

                    # Texto completo do cartão para detecção refinada
                    card_texto = ""
                    try:
                        card_texto = card.inner_text()
                    except Exception:
                        pass

                    # Detecção do Modelo de Trabalho (Presencial, Híbrido ou Remoto)
                    modelo_vaga = detectar_modelo_trabalho(
                        card_texto=card_texto,
                        titulo=titulo,
                        localidade=localidade_bruta,
                    )
                    localidade_limpa = limpar_localidade(localidade_bruta)

                    # Link de Candidatura
                    link_elem = (
                        card.query_selector("a.base-card__full-link")
                        or card.query_selector("a.base-search-card--link")
                        or card.query_selector("a[data-tracking-control-name*='job']")
                        or card.query_selector("a")
                    )
                    raw_link = link_elem.get_attribute("href") if link_elem else ""
                    link = raw_link.split("?")[0] if raw_link and "?" in raw_link else raw_link

                    if titulo and titulo != "Título não informado" and link:
                        vagas_encontradas.append({
                            "Título da Vaga": titulo,
                            "Empresa": empresa,
                            "Localidade": localidade_limpa,
                            "Modelo de Trabalho": modelo_vaga,
                            "Link": link,
                        })

                except Exception:
                    continue

        except PlaywrightTimeoutError:
            pass
        finally:
            context.close()
            browser.close()

    return vagas_encontradas
