"""
Aplicação Streamlit - Sistema Preditivo de Obesidade
Tech Challenge
"""
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.load_model import load_trained_model, load_preprocessor
from src.data_preprocessing import DataPreprocessor

# Configuração da página
st.set_page_config(
    page_title="Sistema Preditivo de Obesidade",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Adicionar meta tag para idioma português brasileiro
st.markdown("""
<meta name="language" content="pt-BR">
<meta http-equiv="content-language" content="pt-BR">
""", unsafe_allow_html=True)

# CSS personalizado - Estilo Mananalu (design limpo, minimalista e estático)
# Script para suprimir avisos do console - executar o mais cedo possível
# Nota: Esses avisos são gerados pelo Streamlit internamente e são inofensivos
st.markdown("""
<script>
// Executar IMEDIATAMENTE usando IIFE
(function() {
    'use strict';
    
    // Definir idioma da página como português brasileiro
    if (document.documentElement) {
        document.documentElement.setAttribute('lang', 'pt-BR');
    }
    // Também definir no body se existir
    if (document.body) {
        document.body.setAttribute('lang', 'pt-BR');
    }
    // Garantir que seja aplicado mesmo após carregamento
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            if (document.documentElement) {
                document.documentElement.setAttribute('lang', 'pt-BR');
            }
        });
    }
    
    // Capturar referências originais
    const _originalError = window.console.error;
    const _originalWarn = window.console.warn;
    
    // Função para verificar se deve suprimir
    function shouldSuppress(msg) {
        if (!msg) return false;
        const s = String(msg).toLowerCase();
        return s.includes('invalid color passed for widgetbackgroundcolor') ||
               s.includes('invalid color passed for widgetbordercolor') ||
               s.includes('invalid color passed for skeletonbackgroundcolor');
    }
    
    // Sobrescrever console.error de forma mais agressiva
    try {
        window.console.error = function(...args) {
            const msg = args[0];
            if (shouldSuppress(msg)) return;
            _originalError.apply(console, args);
        };
    } catch(e) {}
    
    // Sobrescrever console.warn
    try {
        window.console.warn = function(...args) {
            const msg = args[0];
            if (shouldSuppress(msg)) return;
            _originalWarn.apply(console, args);
        };
    } catch(e) {}
    
    // Reaplicar após um delay para garantir que sobrescreve qualquer código posterior
    setTimeout(function() {
        try {
            window.console.error = function(...args) {
                const msg = args[0];
                if (shouldSuppress(msg)) return;
                _originalError.apply(console, args);
            };
            window.console.warn = function(...args) {
                const msg = args[0];
                if (shouldSuppress(msg)) return;
                _originalWarn.apply(console, args);
            };
        } catch(e) {}
    }, 0);
})();
</script>
<style>
    /* ============================================
       ESTILO MANANALU - Design Limpo e Minimalista
       Inspirado em: https://mananalu.boomerangwater.com/
       ============================================ */
    
    /* ============================================
       PALETA DE CORES - Estático (sem dark mode)
       ============================================ */
    :root {
        /* Backgrounds - tons neutros claros e limpos */
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-sidebar: #f1f5f9;
        --bg-card: #ffffff;
        --bg-hover: #f8fafc;
        
        /* Textos - tons escuros suaves e legíveis */
        --text-primary: #1e293b;
        --text-secondary: #475569;
        --text-muted: #64748b;
        --text-light: #94a3b8;
        
        /* Azuis - inspirados em água/oceano (tema sustentabilidade) */
        --accent-blue: #0ea5e9;
        --accent-blue-light: #38bdf8;
        --accent-blue-dark: #0284c7;
        --accent-blue-soft: #e0f2fe;
        --accent-blue-softer: #f0f9ff;
        
        /* Inputs - fundos brancos com bordas suaves */
        --input-bg: #ffffff;
        --input-bg-hover: #f8fafc;
        --input-bg-focus: #f1f5f9;
        --input-border: #e2e8f0;
        --input-border-hover: #cbd5e1;
        --input-border-focus: #0ea5e9;
        --input-text: #1e293b;
        --input-placeholder: #94a3b8;
        
        /* Menu */
        --menu-bg: #f1f5f9;
        --menu-link: #475569;
        --menu-link-hover: #0ea5e9;
        --menu-link-active-bg: #0ea5e9;
        --menu-link-active-text: #ffffff;
        
        /* Filtros */
        --filter-bg: #0ea5e9;
        --filter-text: #ffffff;
        
        /* Bordas e sombras */
        --border-color: #e2e8f0;
        --border-light: #f1f5f9;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Background das páginas */
    .main,
    .stApp,
    .stApp > header,
    .stApp > header > div,
    header[data-testid="stHeader"],
    header[data-testid="stHeader"] > div {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }
    
    /* Header do Streamlit (menu superior) - forçar background claro */
    header[data-testid="stHeader"],
    header[data-testid="stHeader"] > div,
    header[data-testid="stHeader"] > div > div,
    header[data-testid="stHeader"] > div > div > div,
    div[data-testid="stHeader"],
    .stApp > header,
    .stApp > header > div,
    .stApp > header > div > div {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: var(--text-primary) !important;
    }
    
    /* Botões e elementos do header */
    header[data-testid="stHeader"] button,
    header[data-testid="stHeader"] svg,
    header[data-testid="stHeader"] a,
    header[data-testid="stHeader"] span,
    header[data-testid="stHeader"] div {
        color: var(--text-primary) !important;
    }
    
    /* Toolbar do Streamlit (menu hamburger, settings, etc.) */
    .stToolbar,
    .stToolbar > div,
    button[data-testid="baseButton-header"],
    button[aria-label*="Settings"],
    button[aria-label*="Menu"] {
        background-color: #FFFFFF !important;
        color: var(--text-primary) !important;
    }
    
    /* ============================================
       SIDEBAR - CSS SIMPLIFICADO E LIMPO
       ============================================ */
    
    /* Background base do sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        width: 350px !important;
    }
    
    /* Elementos vazios do Streamlit - esconder */
    [data-testid="stSidebar"] div.st-emotion-cache-yenxwz:empty,
    [data-testid="stSidebar"] div.e6f82ta3:empty,
    [data-testid="stSidebar"] div[class*="st-emotion-cache-yenxwz"]:empty,
    [data-testid="stSidebar"] div[class*="e6f82ta3"]:empty {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Elementos do Streamlit no sidebar - garantir visibilidade */
    [data-testid="stSidebar"] [data-testid*="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid*="stVerticalBlock"],
    [data-testid="stSidebar"] [data-testid*="stHorizontalBlock"] {
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
        height: auto !important;
        overflow: visible !important;
    }
    
    /* Iframe do option_menu - garantir visibilidade completa */
    [data-testid="stSidebar"] iframe {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        height: auto !important;
        min-height: 200px !important;
        width: 100% !important;
        border: none !important;
        background: transparent !important;
        z-index: 10 !important;
        position: relative !important;
        overflow: visible !important;
    }
    
    /* Container do menu option_menu - FORÇAR BACKGROUND CLARO (especialmente no Streamlit Cloud) */
    [data-testid="stSidebar"] div[class*="container-xxl"],
    [data-testid="stSidebar"] div[class*="option-menu"],
    [data-testid="stSidebar"] div[class*="container-xxl"] > div,
    [data-testid="stSidebar"] div[class*="container-xxl"] ul,
    [data-testid="stSidebar"] div[class*="container-xxl"] li {
        background: var(--bg-sidebar) !important;
        background-color: var(--bg-sidebar) !important;
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
        height: auto !important;
        overflow: visible !important;
    }
    
    /* Forçar background claro no iframe do option_menu (Streamlit Cloud) */
    [data-testid="stSidebar"] iframe body,
    [data-testid="stSidebar"] iframe html,
    [data-testid="stSidebar"] iframe body > div,
    [data-testid="stSidebar"] iframe body > div > div {
        background: var(--bg-sidebar) !important;
        background-color: var(--bg-sidebar) !important;
    }
    
    /* Forçar background claro em TODOS os elementos dentro do iframe do menu */
    [data-testid="stSidebar"] iframe body div[class*="container-xxl"],
    [data-testid="stSidebar"] iframe body div[class*="container"],
    [data-testid="stSidebar"] iframe body ul[class*="nav-pills"],
    [data-testid="stSidebar"] iframe body li[class*="nav-item"],
    [data-testid="stSidebar"] iframe body a[class*="nav-link"] {
        background: var(--bg-sidebar) !important;
        background-color: var(--bg-sidebar) !important;
    }
    
    /* Elementos do menu - garantir visibilidade */
    [data-testid="stSidebar"] ul[class*="nav-pills"],
    [data-testid="stSidebar"] li[class*="nav-item"],
    [data-testid="stSidebar"] a[class*="nav-link"] {
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
        height: auto !important;
        overflow: visible !important;
        white-space: normal !important;
        text-overflow: clip !important;
    }
    
    h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* Títulos das páginas */
    h1 {
        color: #ffffff !important;
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-blue-light) 100%) !important;
        padding: 0.75rem 1.25rem !important;
        border-radius: 8px !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
        font-size: 1.75rem !important;
        letter-spacing: -0.02em !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Headers (h2) */
    h2 {
        color: #ffffff !important;
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-blue-light) 100%) !important;
        padding: 0.625rem 1rem !important;
        border-radius: 8px !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        letter-spacing: -0.01em !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    /* Subheaders (h3) */
    h3 {
        color: var(--accent-blue) !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 0.75rem !important;
        font-size: 1.25rem !important;
        letter-spacing: -0.01em !important;
    }
    
    /* H3 no sidebar - garantir visibilidade */
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] h3 {
        color: var(--accent-blue) !important;
        font-weight: 600 !important;
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
        height: auto !important;
        margin-top: 1rem !important;
        margin-bottom: 0.75rem !important;
        font-size: 1.25rem !important;
        overflow: visible !important;
        white-space: normal !important;
    }
    
    /* Markdowns no sidebar - garantir visibilidade completa */
    [data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] {
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
        height: auto !important;
        overflow: visible !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    [data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] ul,
    [data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] li,
    [data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] strong {
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
        color: var(--text-primary) !important;
        overflow: visible !important;
        white-space: normal !important;
        text-overflow: clip !important;
    }
    
    [data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] ul {
        list-style-type: disc !important;
        padding-left: 1.5rem !important;
        margin: 0.5rem 0 !important;
    }
    
    [data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] li {
        display: list-item !important;
        margin: 0.25rem 0 !important;
    }
    
    
    /* Menu navigation links - não ativos - usar cor do texto normal e garantir visibilidade completa */
    [data-testid="stSidebar"] [class*="nav-link"]:not([class*="active"]):not([class*="selected"]),
    [data-testid="stSidebar"] a[class*="nav-link"]:not([class*="active"]):not([class*="selected"]),
    [data-testid="stSidebar"] ul[class*="nav-pills"] a:not([class*="active"]),
    [data-testid="stSidebar"] li[class*="nav-item"] a:not([class*="active"]),
    [data-testid="stSidebar"] a.nav-link:not(.active) {
        color: var(--text-primary) !important;
        background-color: transparent !important;
        transition: all 0.2s ease !important;
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
        height: auto !important;
        overflow: visible !important;
        white-space: normal !important;
        text-overflow: clip !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* Remover cor branca dos links não ativos - máxima especificidade */
    [data-testid="stSidebar"] a.nav-link:not(.active),
    [data-testid="stSidebar"] a.nav-link:not(.active)[style*="color: rgb(255, 255, 255)"],
    [data-testid="stSidebar"] a.nav-link:not(.active)[style*="color: white"] {
        color: var(--text-primary) !important;
    }
    
    /* Ícones e elementos filhos dos links não ativos - mesma cor do texto */
    [data-testid="stSidebar"] a.nav-link:not(.active) *,
    [data-testid="stSidebar"] a.nav-link:not(.active) span,
    [data-testid="stSidebar"] a.nav-link:not(.active) i,
    [data-testid="stSidebar"] a.nav-link:not(.active) svg,
    [data-testid="stSidebar"] [class*="nav-link"]:not([class*="active"]):not([class*="selected"]) i,
    [data-testid="stSidebar"] [class*="nav-link"]:not([class*="active"]):not([class*="selected"]) * {
        color: var(--text-primary) !important;
    }
    
    /* Links não ativos - hover */
    [data-testid="stSidebar"] [class*="nav-link"]:not([class*="active"]):not([class*="selected"]):hover,
    [data-testid="stSidebar"] a[class*="nav-link"]:not([class*="active"]):not([class*="selected"]):hover {
        color: var(--menu-link-hover) !important;
        background-color: var(--bg-hover) !important;
    }
    
    /* Links não ativos - forçar cor em todos os elementos filhos */
    [data-testid="stSidebar"] [class*="nav-link"]:not([class*="active"]):not([class*="selected"]) *,
    [data-testid="stSidebar"] a[class*="nav-link"]:not([class*="active"]):not([class*="selected"]) *,
    [data-testid="stSidebar"] ul[class*="nav-pills"] a:not([class*="active"]) *,
    [data-testid="stSidebar"] li[class*="nav-item"] a:not([class*="active"]) * {
        color: inherit !important;
    }
    
    /* Link ativo/selecionado */
    [data-testid="stSidebar"] [class*="nav-link"][class*="active"],
    [data-testid="stSidebar"] [class*="nav-link-selected"],
    [data-testid="stSidebar"] a[class*="nav-link"][class*="active"],
    [data-testid="stSidebar"] a[class*="nav-link-selected"],
    [data-testid="stSidebar"] ul[class*="nav-pills"] a[class*="active"],
    [data-testid="stSidebar"] a.nav-link.active {
        background-color: rgba(0, 92, 169, 0.9) !important;
        color: var(--menu-link-active-text) !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
    }
    
    /* Link ativo - hover (manter texto e hover como estão) */
    [data-testid="stSidebar"] a.nav-link.active:hover,
    [data-testid="stSidebar"] [class*="nav-link"][class*="active"]:hover {
        background-color: rgba(0, 92, 169, 0.9) !important;
        color: var(--menu-link-active-text) !important;
    }
    
    [data-testid="stSidebar"] [class*="nav-link"][class*="active"] *:not(i.icon.bi-house):not(i.icon.bi-activity):not(i.icon.bi-graph-up):not(i.bi-house):not(i.bi-activity):not(i.bi-graph-up):not(i.icon),
    [data-testid="stSidebar"] [class*="nav-link-selected"] *:not(i.icon.bi-house):not(i.icon.bi-activity):not(i.icon.bi-graph-up):not(i.bi-house):not(i.bi-activity):not(i.bi-graph-up):not(i.icon),
    [data-testid="stSidebar"] a.nav-link.active *:not(i.icon.bi-house):not(i.icon.bi-activity):not(i.icon.bi-graph-up):not(i.bi-house):not(i.bi-activity):not(i.bi-graph-up):not(i.icon) {
        color: var(--menu-link-active-text) !important;
    }
    
    /* Ícones Bootstrap Icons - brancos apenas quando link ativo - REGRA FINAL COM MÁXIMA ESPECIFICIDADE */
    /* Esta regra DEVE vir por último para sobrescrever TODOS os outros estilos */
    /* Usando seletores com máxima especificidade possível */
    html body [data-testid="stSidebar"] div.container-xxl ul.nav-pills li.nav-item a.nav-link.active i.icon.bi-house,
    html body [data-testid="stSidebar"] div.container-xxl ul.nav-pills li.nav-item a.nav-link.active i.icon.bi-activity,
    html body [data-testid="stSidebar"] div.container-xxl ul.nav-pills li.nav-item a.nav-link.active i.icon.bi-graph-up,
    html body [data-testid="stSidebar"] div.container-xxl ul.nav-pills li.nav-item a[class*="nav-link"][class*="active"] i.icon.bi-house,
    html body [data-testid="stSidebar"] div.container-xxl ul.nav-pills li.nav-item a[class*="nav-link"][class*="active"] i.icon.bi-activity,
    html body [data-testid="stSidebar"] div.container-xxl ul.nav-pills li.nav-item a[class*="nav-link"][class*="active"] i.icon.bi-graph-up,
    html body [data-testid="stSidebar"] a.nav-link.active i.icon.bi-house,
    html body [data-testid="stSidebar"] a.nav-link.active i.icon.bi-activity,
    html body [data-testid="stSidebar"] a.nav-link.active i.icon.bi-graph-up,
    html body [data-testid="stSidebar"] a[class*="nav-link"][class*="active"] i.icon.bi-house,
    html body [data-testid="stSidebar"] a[class*="nav-link"][class*="active"] i.icon.bi-activity,
    html body [data-testid="stSidebar"] a[class*="nav-link"][class*="active"] i.icon.bi-graph-up,
    html body [data-testid="stSidebar"] a[class*="nav-link-selected"] i.icon.bi-house,
    html body [data-testid="stSidebar"] a[class*="nav-link-selected"] i.icon.bi-activity,
    html body [data-testid="stSidebar"] a[class*="nav-link-selected"] i.icon.bi-graph-up,
    html body [data-testid="stSidebar"] a.nav-link.active i.bi-house,
    html body [data-testid="stSidebar"] a.nav-link.active i.bi-activity,
    html body [data-testid="stSidebar"] a.nav-link.active i.bi-graph-up,
    html body [data-testid="stSidebar"] a.nav-link.active i.icon {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        fill: #ffffff !important;
    }
    
    /* Pseudo-elementos ::before dos ícones em links ativos - REGRA FINAL COM MÁXIMA ESPECIFICIDADE */
    html body [data-testid="stSidebar"] div.container-xxl ul.nav-pills li.nav-item a.nav-link.active i.icon.bi-house::before,
    html body [data-testid="stSidebar"] div.container-xxl ul.nav-pills li.nav-item a.nav-link.active i.icon.bi-activity::before,
    html body [data-testid="stSidebar"] div.container-xxl ul.nav-pills li.nav-item a.nav-link.active i.icon.bi-graph-up::before,
    html body [data-testid="stSidebar"] div.container-xxl ul.nav-pills li.nav-item a[class*="nav-link"][class*="active"] i.icon.bi-house::before,
    html body [data-testid="stSidebar"] div.container-xxl ul.nav-pills li.nav-item a[class*="nav-link"][class*="active"] i.icon.bi-activity::before,
    html body [data-testid="stSidebar"] div.container-xxl ul.nav-pills li.nav-item a[class*="nav-link"][class*="active"] i.icon.bi-graph-up::before,
    html body [data-testid="stSidebar"] a.nav-link.active i.icon.bi-house::before,
    html body [data-testid="stSidebar"] a.nav-link.active i.icon.bi-activity::before,
    html body [data-testid="stSidebar"] a.nav-link.active i.icon.bi-graph-up::before,
    html body [data-testid="stSidebar"] a[class*="nav-link"][class*="active"] i.icon.bi-house::before,
    html body [data-testid="stSidebar"] a[class*="nav-link"][class*="active"] i.icon.bi-activity::before,
    html body [data-testid="stSidebar"] a[class*="nav-link"][class*="active"] i.icon.bi-graph-up::before,
    html body [data-testid="stSidebar"] a[class*="nav-link-selected"] i.icon.bi-house::before,
    html body [data-testid="stSidebar"] a[class*="nav-link-selected"] i.icon.bi-activity::before,
    html body [data-testid="stSidebar"] a[class*="nav-link-selected"] i.icon.bi-graph-up::before,
    html body [data-testid="stSidebar"] a.nav-link.active i.bi-house::before,
    html body [data-testid="stSidebar"] a.nav-link.active i.bi-activity::before,
    html body [data-testid="stSidebar"] a.nav-link.active i.bi-graph-up::before {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        fill: #ffffff !important;
    }
    
    /* Filtros */
    div[style*="background-color: #005ca9e6"],
    div[style*="background-color: #0ea5e9"] {
        background-color: var(--filter-bg) !important;
        padding: 1rem 1.25rem !important;
        border-radius: 8px !important;
        margin-bottom: 1rem !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    div[style*="background-color: #005ca9e6"] h2,
    div[style*="background-color: #005ca9e6"] h3,
    div[style*="background-color: #0ea5e9"] h2,
    div[style*="background-color: #0ea5e9"] h3 {
        color: var(--filter-text) !important;
        font-weight: 600 !important;
        margin: 0 0 0.75rem 0 !important;
    }
    
    div[style*="background-color: #005ca9e6"] label,
    div[style*="background-color: #0ea5e9"] label {
        color: var(--filter-text) !important;
    }
    
    div[style*="background-color: #005ca9e6"] .stTextInput > div > div > input,
    div[style*="background-color: #005ca9e6"] .stNumberInput > div > div > input,
    div[style*="background-color: #0ea5e9"] .stTextInput > div > div > input,
    div[style*="background-color: #0ea5e9"] .stNumberInput > div > div > input {
        background-color: #ffffff !important;
        color: var(--input-text) !important;
    }
    
    /* Botões - primary e secondary com mesmo estilo */
    .stButton > button,
    button[data-testid="baseButton-primary"],
    button[data-testid="baseButton-secondary"],
    button[data-testid="stBaseButton-primary"],
    button[data-testid="stBaseButton-secondary"] {
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-blue-light) 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: var(--shadow-md) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover,
    button[data-testid="baseButton-primary"]:hover,
    button[data-testid="baseButton-secondary"]:hover,
    button[data-testid="stBaseButton-primary"]:hover,
    button[data-testid="stBaseButton-secondary"]:hover {
        background: linear-gradient(135deg, var(--accent-blue-dark) 0%, var(--accent-blue) 100%) !important;
        box-shadow: var(--shadow-lg) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Cards de métricas */
    .metric-card {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        box-shadow: var(--shadow-sm) !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Result box */
    .result-box {
        background-color: #005ca9e6 !important;
        color: #ffffff !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        box-shadow: var(--shadow-lg) !important;
        margin: 1rem 0 !important;
    }
    
    /* Info boxes */
    .info-box {
        background-color: var(--accent-blue-softer) !important;
        border-left: 4px solid var(--accent-blue) !important;
        border-radius: 6px !important;
        padding: 1rem !important;
        margin: 0.75rem 0 !important;
    }
    
    /* REGRA FINAL: Garantir que TODOS os elementos do sidebar sejam visíveis e não cortados */
    [data-testid="stSidebar"] * {
        max-width: 100% !important;
        box-sizing: border-box !important;
        overflow: visible !important;
    }
    
    /* Exceção: apenas elementos específicos podem ter overflow diferente */
    [data-testid="stSidebar"] iframe {
        overflow: visible !important;
    }
    
    /* Garantir que elementos do Streamlit não sejam cortados */
    [data-testid="stSidebar"] [data-testid*="st"] {
        max-width: 100% !important;
        width: 100% !important;
        box-sizing: border-box !important;
        overflow: visible !important;
        white-space: normal !important;
    }
    
    /* Logo/título do sidebar - garantir visibilidade completa */
    [data-testid="stSidebar"] .logo-title,
    [data-testid="stSidebar"] div.logo-title,
    [data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] .logo-title {
        color: #ffffff !important;
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-blue-light) 100%) !important;
        padding: 0.75rem 1.25rem !important;
        border-radius: 8px !important;
        text-align: center !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        letter-spacing: -0.02em !important;
        box-shadow: var(--shadow-md) !important;
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
        height: auto !important;
        min-height: auto !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        overflow: visible !important;
        white-space: normal !important;
        word-wrap: break-word !important;
    }
    
    [data-testid="stSidebar"] .logo-title *,
    [data-testid="stSidebar"] div.logo-title *,
    [data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] .logo-title * {
        color: #ffffff !important;
        visibility: visible !important;
        display: inline !important;
        opacity: 1 !important;
        white-space: normal !important;
    }
    
    /* Checkboxes */
    .stCheckbox input[type="checkbox"] {
        accent-color: var(--accent-blue) !important;
    }
    
    .stCheckbox input[type="checkbox"]:checked {
        background-color: var(--accent-blue) !important;
        border-color: var(--accent-blue) !important;
    }
    
    .stCheckbox label {
        color: var(--text-primary) !important;
        font-weight: 400 !important;
    }
    
    /* Campos de input */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextInput input,
    .stNumberInput input {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 1.5px solid var(--input-border) !important;
        border-radius: 8px !important;
        padding: 0.625rem 0.875rem !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stNumberInput > div > div > input::placeholder,
    .stTextInput input::placeholder,
    .stNumberInput input::placeholder {
        color: var(--input-placeholder) !important;
        opacity: 1 !important;
    }
    
    .stTextInput > div > div > input:hover,
    .stNumberInput > div > div > input:hover,
    .stTextInput input:hover,
    .stNumberInput input:hover {
        background-color: var(--input-bg-hover) !important;
        border-color: var(--input-border-hover) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextInput input:focus,
    .stNumberInput input:focus {
        background-color: var(--input-bg-focus) !important;
        border-color: var(--input-border-focus) !important;
        box-shadow: 0 0 0 3px var(--accent-blue-soft) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input:not(:placeholder-shown),
    .stNumberInput > div > div > input:not(:placeholder-shown),
    .stTextInput input:not(:placeholder-shown),
    .stNumberInput input:not(:placeholder-shown) {
        color: var(--input-text) !important;
        font-weight: 500 !important;
    }
    
    /* Labels */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div > div[data-baseweb="select"],
    .stSelectbox > div > div > div,
    div[data-baseweb="select"] > div {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 1.5px solid var(--input-border) !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        transition: all 0.2s ease !important;
    }
    
    .stSelectbox > div > div > div[data-baseweb="select"]:hover,
    div[data-baseweb="select"] > div:hover {
        background-color: var(--input-bg-hover) !important;
        border-color: var(--input-border-hover) !important;
    }
    
    div[data-baseweb="select"] span,
    .stSelectbox span {
        color: var(--input-text) !important;
    }
    
    /* Multiselect - tags */
    div[data-baseweb="tag"],
    span[data-baseweb="tag"] {
        background-color: rgba(0, 92, 169, 0.9) !important;
        color: rgb(255, 255, 255) !important;
        border: none !important;
    }
    
    /* Texto dentro das tags */
    span[data-baseweb="tag"] span,
    span[data-baseweb="tag"] span[title] {
        color: rgb(255, 255, 255) !important;
    }
    
    /* Ícone de fechar nas tags */
    span[data-baseweb="tag"] svg,
    span[data-baseweb="tag"] path {
        fill: rgb(255, 255, 255) !important;
        stroke: rgb(255, 255, 255) !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background-color: var(--accent-blue) !important;
    }
    
    .stSlider [data-baseweb="slider-handle"],
    .stSlider button[role="slider"] {
        background-color: var(--accent-blue) !important;
        border: 2px solid #ffffff !important;
    }
    
    .stSlider > div > div > span,
    .stSlider span:not(label span) {
        color: var(--accent-blue) !important;
        font-weight: 600 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: var(--accent-blue-softer) !important;
        color: var(--accent-blue) !important;
        border-radius: 6px !important;
        padding: 0.75rem 1rem !important;
        font-weight: 500 !important;
    }
    
    /* Tabelas */
    .dataframe {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    /* Alerts */
    .stAlert {
        border-left: 4px solid var(--accent-blue) !important;
        border-radius: 6px !important;
    }
    
    /* Regras finais - máxima especificidade */
    .main .stTextInput > div > div > input,
    .main .stNumberInput > div > div > input,
    .stApp .stTextInput > div > div > input,
    .stApp .stNumberInput > div > div > input {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 1.5px solid var(--input-border) !important;
    }
    
    .main .stSelectbox > div > div > div[data-baseweb="select"],
    .stApp .stSelectbox > div > div > div[data-baseweb="select"] {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 1.5px solid var(--input-border) !important;
    }
    
    /* Sobrescrever border-color do elemento st-emotion-cache-upotea */
    .st-emotion-cache-upotea {
        border-color: #e2e8f0 !important;
    }
    
    /* Texto dos botões - cor branca */
    .stDownloadButton button p,
    .stDownloadButton button span,
    .stDownloadButton p,
    .stDownloadButton span,
    .stButton button p,
    .stButton button span,
    button[data-testid="baseButton-secondary"] p,
    button[data-testid="baseButton-secondary"] span,
    button[data-testid="baseButton-secondary"] *,
    button[data-testid="baseButton-primary"] p,
    button[data-testid="baseButton-primary"] span,
    button[data-testid="baseButton-primary"] *,
    button[type="submit"] p,
    button[type="submit"] span {
        color: #ffffff !important;
    }
</style>
<script>
(function() {
    // Função para forçar ícones Bootstrap Icons a ficarem brancos em links ativos
    function fixActiveIcons() {
        const activeLinks = document.querySelectorAll(
            '[data-testid="stSidebar"] a.nav-link.active, ' +
            '[data-testid="stSidebar"] a[class*="nav-link"][class*="active"], ' +
            '[data-testid="stSidebar"] a[class*="nav-link-selected"]'
        );
        
        activeLinks.forEach(function(link) {
            // Buscar TODOS os ícones possíveis, incluindo i.icon.bi-*
            const icons = link.querySelectorAll('i.bi-house, i.bi-activity, i.bi-graph-up, i.icon, i.icon.bi-house, i.icon.bi-activity, i.icon.bi-graph-up, i[class*="bi-"], i');
            icons.forEach(function(icon) {
                // Verificar se é um ícone Bootstrap (incluindo i.icon.bi-*)
                const hasBiClass = Array.from(icon.classList).some(cls => cls.startsWith('bi-'));
                const hasIconClass = icon.classList.contains('icon');
                if (hasBiClass || hasIconClass) {
                    // MÉTODO 1: Remover completamente o atributo style
                    icon.removeAttribute('style');
                    
                    // MÉTODO 2: Forçar cor branca usando setProperty com important
                    icon.style.setProperty('color', '#ffffff', 'important');
                    icon.style.setProperty('-webkit-text-fill-color', '#ffffff', 'important');
                    icon.style.setProperty('fill', '#ffffff', 'important');
                    
                    // MÉTODO 3: Usar setAttribute diretamente (sobrescreve tudo)
                    icon.setAttribute('style', 'color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; fill: #ffffff !important;');
                    
                    // MÉTODO 4: Criar uma classe CSS dinâmica e aplicá-la
                    if (!document.getElementById('force-white-icons')) {
                        const style = document.createElement('style');
                        style.id = 'force-white-icons';
                        style.textContent = `
                            [data-testid="stSidebar"] a.nav-link.active i.icon.bi-house,
                            [data-testid="stSidebar"] a.nav-link.active i.icon.bi-activity,
                            [data-testid="stSidebar"] a.nav-link.active i.icon.bi-graph-up {
                                color: #ffffff !important;
                                -webkit-text-fill-color: #ffffff !important;
                                fill: #ffffff !important;
                            }
                        `;
                        document.head.appendChild(style);
                    }
                }
            });
        });
        
        // Criar estilo global para pseudo-elementos ::before dos ícones ativos
        let styleId = 'bootstrap-icons-active-fix';
        let style = document.getElementById(styleId);
        if (!style) {
            style = document.createElement('style');
            style.id = styleId;
            document.head.appendChild(style);
        }
        
        // Adicionar regras para todos os ícones Bootstrap em links ativos (incluindo i.icon.bi-*)
        // Usando seletores com máxima especificidade para sobrescrever estilos herdados
        style.textContent = `
            [data-testid="stSidebar"] a.nav-link.active[class*="nav-link"] i.icon.bi-house::before,
            [data-testid="stSidebar"] a.nav-link.active[class*="nav-link"] i.icon.bi-activity::before,
            [data-testid="stSidebar"] a.nav-link.active[class*="nav-link"] i.icon.bi-graph-up::before,
            [data-testid="stSidebar"] a[class*="nav-link"][class*="active"][class*="nav-link"] i.icon.bi-house::before,
            [data-testid="stSidebar"] a[class*="nav-link"][class*="active"][class*="nav-link"] i.icon.bi-activity::before,
            [data-testid="stSidebar"] a[class*="nav-link"][class*="active"][class*="nav-link"] i.icon.bi-graph-up::before,
            [data-testid="stSidebar"] a[class*="nav-link-selected"][class*="nav-link"] i.icon.bi-house::before,
            [data-testid="stSidebar"] a[class*="nav-link-selected"][class*="nav-link"] i.icon.bi-activity::before,
            [data-testid="stSidebar"] a[class*="nav-link-selected"][class*="nav-link"] i.icon.bi-graph-up::before,
            [data-testid="stSidebar"] ul.nav-pills a.nav-link.active i.icon.bi-house::before,
            [data-testid="stSidebar"] ul.nav-pills a.nav-link.active i.icon.bi-activity::before,
            [data-testid="stSidebar"] ul.nav-pills a.nav-link.active i.icon.bi-graph-up::before,
            [data-testid="stSidebar"] li.nav-item a.nav-link.active i.icon.bi-house::before,
            [data-testid="stSidebar"] li.nav-item a.nav-link.active i.icon.bi-activity::before,
            [data-testid="stSidebar"] li.nav-item a.nav-link.active i.icon.bi-graph-up::before,
            [data-testid="stSidebar"] a.nav-link.active i.bi-house::before,
            [data-testid="stSidebar"] a.nav-link.active i.bi-activity::before,
            [data-testid="stSidebar"] a.nav-link.active i.bi-graph-up::before {
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
            }
        `;
    }
    
    function fixNavLinks() {
        // Remover cor branca dos links não ativos e aplicar cor do texto normal
        const nonActiveLinks = document.querySelectorAll('[data-testid="stSidebar"] a.nav-link:not(.active)');
        const textColor = getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim() || '#1e293b';
        
        nonActiveLinks.forEach(function(link) {
            // Forçar cor do texto normal no link
            if (link.style.color === 'rgb(255, 255, 255)' || link.style.color === 'white' || link.style.color === '#ffffff') {
                link.style.setProperty('color', textColor, 'important');
            }
            
            // Forçar cor do texto normal em todos os filhos (ícones, spans, etc.)
            const children = link.querySelectorAll('*');
            children.forEach(function(child) {
                if (child.style.color === 'rgb(255, 255, 255)' || child.style.color === 'white' || child.style.color === '#ffffff') {
                    child.style.setProperty('color', textColor, 'important');
                }
            });
        });
        
        // Fix ícones ativos
        fixActiveIcons();
    }
    
    // Garantir que o idioma seja definido
    function setLanguage() {
        if (document.documentElement) {
            document.documentElement.setAttribute('lang', 'pt-BR');
        }
        if (document.body) {
            document.body.setAttribute('lang', 'pt-BR');
        }
        // Adicionar meta tag se não existir
        if (!document.querySelector('meta[name="language"]')) {
            const metaLang = document.createElement('meta');
            metaLang.setAttribute('name', 'language');
            metaLang.setAttribute('content', 'pt-BR');
            document.head.appendChild(metaLang);
        }
        if (!document.querySelector('meta[http-equiv="content-language"]')) {
            const metaContentLang = document.createElement('meta');
            metaContentLang.setAttribute('http-equiv', 'content-language');
            metaContentLang.setAttribute('content', 'pt-BR');
            document.head.appendChild(metaContentLang);
        }
    }
    
    // Executar quando o DOM estiver pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setLanguage();
            ensureMenuVisible();
            fixNavLinks();
            fixActiveIcons();
        });
    } else {
        setLanguage();
        ensureMenuVisible();
        fixNavLinks();
        fixActiveIcons();
    }
    
    // Executar após delays para garantir
    setTimeout(function() {
        setLanguage();
        ensureMenuVisible();
        fixNavLinks();
        fixActiveIcons();
    }, 50);
    setTimeout(function() {
        setLanguage();
        ensureMenuVisible();
        fixNavLinks();
        fixActiveIcons();
    }, 100);
    setTimeout(function() {
        setLanguage();
        ensureMenuVisible();
        fixNavLinks();
        fixActiveIcons();
    }, 200);
    setTimeout(function() {
        setLanguage();
        ensureMenuVisible();
        fixNavLinks();
        fixActiveIcons();
    }, 500);
    setTimeout(function() {
        setLanguage();
        ensureMenuVisible();
        fixNavLinks();
        fixActiveIcons();
    }, 1000);
    setTimeout(function() {
        ensureMenuVisible();
    }, 2000);
    
    // Função para garantir que o menu option_menu seja visível
    function ensureMenuVisible() {
        // Procurar TODOS os iframes no sidebar
        const iframes = document.querySelectorAll('[data-testid="stSidebar"] iframe');
        iframes.forEach(function(iframe) {
            // Se for iframe do option_menu ou qualquer iframe no sidebar
            if (!iframe.src || iframe.src.includes('option_menu') || iframe.src.includes('streamlit_option_menu') || iframe.src.includes('component')) {
                iframe.style.setProperty('display', 'block', 'important');
                iframe.style.setProperty('visibility', 'visible', 'important');
                iframe.style.setProperty('opacity', '1', 'important');
                iframe.style.setProperty('height', 'auto', 'important');
                iframe.style.setProperty('min-height', '200px', 'important');
                iframe.style.setProperty('max-height', 'none', 'important');
                iframe.style.setProperty('z-index', '1000', 'important');
                iframe.style.setProperty('position', 'relative', 'important');
                iframe.style.setProperty('width', '100%', 'important');
                iframe.style.setProperty('border', 'none', 'important');
                iframe.style.setProperty('background', 'transparent', 'important');
            }
        });
        
        // Procurar container do menu - TODOS os containers possíveis
        const containers = document.querySelectorAll('[data-testid="stSidebar"] div[class*="container-xxl"], [data-testid="stSidebar"] div[class*="container"]:not([class*="st"]), [data-testid="stSidebar"] div[class*="option-menu"]');
        containers.forEach(function(container) {
            container.style.setProperty('display', 'block', 'important');
            container.style.setProperty('visibility', 'visible', 'important');
            container.style.setProperty('opacity', '1', 'important');
            container.style.setProperty('height', 'auto', 'important');
            container.style.setProperty('min-height', 'auto', 'important');
            container.style.setProperty('max-height', 'none', 'important');
            container.style.setProperty('z-index', '1000', 'important');
            container.style.setProperty('position', 'relative', 'important');
            container.style.setProperty('overflow', 'visible', 'important');
            // FORÇAR BACKGROUND CLARO (especialmente para Streamlit Cloud)
            container.style.setProperty('background', 'var(--bg-sidebar)', 'important');
            container.style.setProperty('background-color', 'var(--bg-sidebar)', 'important');
        });
        
        // Forçar background claro em elementos filhos do container
        containers.forEach(function(container) {
            const children = container.querySelectorAll('div, ul, li');
            children.forEach(function(child) {
                child.style.setProperty('background', 'var(--bg-sidebar)', 'important');
                child.style.setProperty('background-color', 'var(--bg-sidebar)', 'important');
            });
        });
        
        // Forçar background claro dentro do iframe do option_menu (Streamlit Cloud)
        const iframes = document.querySelectorAll('[data-testid="stSidebar"] iframe');
        iframes.forEach(function(iframe) {
            try {
                const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                if (iframeDoc) {
                    const iframeBody = iframeDoc.body;
                    if (iframeBody) {
                        iframeBody.style.setProperty('background', 'var(--bg-sidebar)', 'important');
                        iframeBody.style.setProperty('background-color', 'var(--bg-sidebar)', 'important');
                        
                        const iframeContainers = iframeDoc.querySelectorAll('div[class*="container-xxl"], div[class*="container"], ul[class*="nav-pills"], li[class*="nav-item"]');
                        iframeContainers.forEach(function(iframeContainer) {
                            iframeContainer.style.setProperty('background', 'var(--bg-sidebar)', 'important');
                            iframeContainer.style.setProperty('background-color', 'var(--bg-sidebar)', 'important');
                        });
                    }
                }
            } catch (e) {
                // Cross-origin ou outro erro - ignorar
            }
        });
        
        // Procurar elementos do menu - TODOS os elementos possíveis
        const navPills = document.querySelectorAll('[data-testid="stSidebar"] ul[class*="nav-pills"], [data-testid="stSidebar"] ul[class*="nav"]');
        navPills.forEach(function(ul) {
            ul.style.setProperty('display', 'block', 'important');
            ul.style.setProperty('visibility', 'visible', 'important');
            ul.style.setProperty('opacity', '1', 'important');
            ul.style.setProperty('height', 'auto', 'important');
        });
        
        const navItems = document.querySelectorAll('[data-testid="stSidebar"] li[class*="nav-item"], [data-testid="stSidebar"] li[class*="nav"]');
        navItems.forEach(function(li) {
            li.style.setProperty('display', 'block', 'important');
            li.style.setProperty('visibility', 'visible', 'important');
            li.style.setProperty('opacity', '1', 'important');
        });
        
        const navLinks = document.querySelectorAll('[data-testid="stSidebar"] a[class*="nav-link"], [data-testid="stSidebar"] a[class*="nav"]');
        navLinks.forEach(function(link) {
            link.style.setProperty('display', 'block', 'important');
            link.style.setProperty('visibility', 'visible', 'important');
            link.style.setProperty('opacity', '1', 'important');
            // Aplicar cor baseada no estado (ativo ou não)
            if (link.classList.contains('active') || link.getAttribute('class') && link.getAttribute('class').includes('active')) {
                // Link ativo - manter background azul e texto branco
            } else {
                // Link não ativo - texto escuro e background claro
                link.style.setProperty('color', '#1e293b', 'important');
                link.style.setProperty('background', 'transparent', 'important');
                link.style.setProperty('background-color', 'transparent', 'important');
            }
            link.style.setProperty('height', 'auto', 'important');
            link.style.setProperty('width', '100%', 'important');
            link.style.setProperty('max-width', '100%', 'important');
            link.style.setProperty('overflow', 'visible', 'important');
            link.style.setProperty('white-space', 'normal', 'important');
            link.style.setProperty('text-overflow', 'clip', 'important');
            link.style.setProperty('box-sizing', 'border-box', 'important');
        });
        
        // Forçar cor do texto nos links não ativos dentro do iframe
        iframes.forEach(function(iframe) {
            try {
                const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                if (iframeDoc) {
                    const iframeLinks = iframeDoc.querySelectorAll('a[class*="nav-link"], a[class*="nav"]');
                    iframeLinks.forEach(function(iframeLink) {
                        if (!iframeLink.classList.contains('active') && !iframeLink.getAttribute('class')?.includes('active')) {
                            iframeLink.style.setProperty('color', '#1e293b', 'important');
                            iframeLink.style.setProperty('background', 'transparent', 'important');
                            iframeLink.style.setProperty('background-color', 'transparent', 'important');
                        }
                    });
                }
            } catch (e) {
                // Cross-origin ou outro erro - ignorar
            }
        });
        
        // Procurar spans e textos dentro do menu
        const menuTexts = document.querySelectorAll('[data-testid="stSidebar"] span, [data-testid="stSidebar"] i[class*="bi-"], [data-testid="stSidebar"] i[class*="icon"]');
        menuTexts.forEach(function(text) {
            // Verificar se está dentro de um link do menu
            const parentLink = text.closest('a[class*="nav-link"], a[class*="nav"]');
            if (parentLink) {
                text.style.setProperty('display', 'inline-block', 'important');
                text.style.setProperty('visibility', 'visible', 'important');
                text.style.setProperty('opacity', '1', 'important');
            }
        });
        
        // Garantir que o logo-title seja visível
        const logoTitles = document.querySelectorAll('[data-testid="stSidebar"] .logo-title, [data-testid="stSidebar"] div.logo-title');
        logoTitles.forEach(function(logo) {
            logo.style.setProperty('display', 'block', 'important');
            logo.style.setProperty('visibility', 'visible', 'important');
            logo.style.setProperty('opacity', '1', 'important');
            logo.style.setProperty('height', 'auto', 'important');
            logo.style.setProperty('min-height', 'auto', 'important');
            logo.style.setProperty('width', '100%', 'important');
            logo.style.setProperty('overflow', 'visible', 'important');
            logo.style.setProperty('box-sizing', 'border-box', 'important');
        });
        
        // Garantir que markdowns do Streamlit sejam visíveis (título e "Sobre o Sistema")
        const markdownContainers = document.querySelectorAll('[data-testid="stSidebar"] [data-testid*="stMarkdownContainer"]');
        markdownContainers.forEach(function(container) {
            container.style.setProperty('display', 'block', 'important');
            container.style.setProperty('visibility', 'visible', 'important');
            container.style.setProperty('opacity', '1', 'important');
            container.style.setProperty('height', 'auto', 'important');
            container.style.setProperty('width', '100%', 'important');
            container.style.setProperty('overflow', 'visible', 'important');
            container.style.setProperty('box-sizing', 'border-box', 'important');
        });
        
        // Garantir que h3 (Sobre o Sistema) seja visível
        const h3Elements = document.querySelectorAll('[data-testid="stSidebar"] h3');
        h3Elements.forEach(function(h3) {
            h3.style.setProperty('display', 'block', 'important');
            h3.style.setProperty('visibility', 'visible', 'important');
            h3.style.setProperty('opacity', '1', 'important');
            h3.style.setProperty('color', '#0ea5e9', 'important');
            h3.style.setProperty('height', 'auto', 'important');
            h3.style.setProperty('width', '100%', 'important');
            h3.style.setProperty('max-width', '100%', 'important');
            h3.style.setProperty('overflow', 'visible', 'important');
            h3.style.setProperty('white-space', 'normal', 'important');
            h3.style.setProperty('box-sizing', 'border-box', 'important');
        });
        
        // Garantir que parágrafos e listas sejam visíveis
        const paragraphs = document.querySelectorAll('[data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] p');
        paragraphs.forEach(function(p) {
            p.style.setProperty('display', 'block', 'important');
            p.style.setProperty('visibility', 'visible', 'important');
            p.style.setProperty('opacity', '1', 'important');
            p.style.setProperty('color', '#1e293b', 'important');
            p.style.setProperty('overflow', 'visible', 'important');
            p.style.setProperty('white-space', 'normal', 'important');
        });
        
        const lists = document.querySelectorAll('[data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] ul, [data-testid="stSidebar"] [data-testid*="stMarkdownContainer"] li');
        lists.forEach(function(list) {
            list.style.setProperty('display', 'block', 'important');
            list.style.setProperty('visibility', 'visible', 'important');
            list.style.setProperty('opacity', '1', 'important');
            list.style.setProperty('overflow', 'visible', 'important');
            list.style.setProperty('white-space', 'normal', 'important');
        });
    }
    
    // Observar mudanças no DOM
    const observer = new MutationObserver(function() {
        setLanguage(); // Garantir idioma em mudanças dinâmicas
        ensureMenuVisible(); // Garantir que menu seja visível
        fixNavLinks();
        fixActiveIcons();
    });
    
    if (document.body) {
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['class']
        });
    }
})();
</script>
""", unsafe_allow_html=True)

# Mapeamento de níveis de obesidade para português
OBESITY_LEVELS_PT = {
    'Normal_Weight': 'Peso Normal',
    'Overweight_Level_I': 'Sobrepeso Nível I',
    'Overweight_Level_II': 'Sobrepeso Nível II',
    'Obesity_Type_I': 'Obesidade Tipo I',
    'Obesity_Type_II': 'Obesidade Tipo II',
    'Obesity_Type_III': 'Obesidade Tipo III',
    'Insufficient_Weight': 'Peso Insuficiente'
}

# Traduções para português
TRANSLATIONS = {
    'Gender': {
        'Male': 'Masculino',
        'Female': 'Feminino'
    },
    'family_history': {
        'yes': 'Sim',
        'no': 'Não'
    },
    'FAVC': {
        'yes': 'Sim',
        'no': 'Não'
    },
    'CAEC': {
        'no': 'Não',
        'Sometimes': 'Às vezes',
        'Frequently': 'Frequentemente',
        'Always': 'Sempre'
    },
    'SMOKE': {
        'yes': 'Sim',
        'no': 'Não'
    },
    'SCC': {
        'yes': 'Sim',
        'no': 'Não'
    },
    'CALC': {
        'no': 'Não',
        'Sometimes': 'Às vezes',
        'Frequently': 'Frequentemente',
        'Always': 'Sempre'
    },
    'MTRANS': {
        'Public_Transportation': 'Transporte Público',
        'Automobile': 'Automóvel',
        'Walking': 'Caminhada',
        'Motorbike': 'Motocicleta',
        'Bike': 'Bicicleta'
    }
}

# Função para carregar modelo (com cache)
@st.cache_resource
def load_model():
    """Carrega o modelo e pré-processador"""
    try:
        model = load_trained_model('models/obesity_model.joblib')
        preprocessor_data = load_preprocessor('models/preprocessor.joblib')
        return model, preprocessor_data
    except Exception as e:
        st.error(f"Erro ao carregar modelo: {str(e)}")
        return None, None

# Função para fazer predição
def make_prediction(input_data, model, preprocessor_data):
    """Faz predição usando o modelo treinado"""
    try:
        # Criar DataFrame com os dados de entrada
        df = pd.DataFrame([input_data])
        
        # Pré-processar dados
        preprocessor = DataPreprocessor()
        preprocessor.label_encoders = preprocessor_data['label_encoders']
        preprocessor.scaler = preprocessor_data['scaler']
        preprocessor.feature_names = preprocessor_data['feature_names']
        
        # Aplicar pré-processamento
        df_processed = preprocessor.handle_missing_values(df)
        df_processed = preprocessor.encode_categorical(df_processed, fit=False)
        
        # Criar IMC
        df_processed = preprocessor.create_bmi(df_processed)
        
        # Preparar features (sem target)
        X = df_processed[preprocessor.feature_names]
        
        # Normalizar
        X_scaled = preprocessor.scale_features(X, fit=False)
        
        # Fazer predição
        prediction = model.predict(X_scaled)[0]
        probabilities = model.predict_proba(X_scaled)[0]
        classes = model.classes_
        
        return prediction, probabilities, classes
        
    except Exception as e:
        st.error(f"Erro ao fazer predição: {str(e)}")
        return None, None, None

# Função para gerar PDF
def generate_pdf(medico_nome, medico_crm, paciente_nome, input_data, prediction, probabilities, classes):
    """Gera PDF com o resultado da predição"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12
    )
    
    # Título
    story.append(Paragraph("Relatório de Predição de Obesidade", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Informações do médico e paciente (tratar campos vazios)
    profissional = medico_nome.strip() if medico_nome else "Não informado"
    registro = medico_crm.strip() if medico_crm else "Não informado"
    paciente = paciente_nome.strip() if paciente_nome else "Não informado"
    
    info_data = [
        ['Profissional:', profissional],
        ['Registro do Conselho:', registro],
        ['Paciente:', paciente],
        ['Data:', datetime.now().strftime('%d/%m/%Y %H:%M')]
    ]
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Resultado da predição
    prediction_pt = OBESITY_LEVELS_PT.get(prediction, prediction)
    pred_idx = list(classes).index(prediction)
    confidence = probabilities[pred_idx] * 100
    
    story.append(Paragraph("Resultado da Predição", heading_style))
    story.append(Paragraph(f"<b>Nível de Obesidade:</b> {prediction_pt}", styles['Normal']))
    story.append(Paragraph(f"<b>Confiança:</b> {confidence:.2f}%", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Probabilidades
    story.append(Paragraph("Probabilidades por Classe", heading_style))
    prob_data = [['Nível de Obesidade', 'Probabilidade (%)']]
    prob_df = pd.DataFrame({
        'Nível': [OBESITY_LEVELS_PT.get(c, c) for c in classes],
        'Probabilidade': [p * 100 for p in probabilities]
    }).sort_values('Probabilidade', ascending=False)
    
    for _, row in prob_df.iterrows():
        prob_data.append([row['Nível'], f"{row['Probabilidade']:.2f}%"])
    
    prob_table = Table(prob_data, colWidths=[3.5*inch, 2.5*inch])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    story.append(prob_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Dados do paciente
    story.append(Paragraph("Dados do Paciente", heading_style))
    
    # Mapeamento de tradução dos campos
    field_translations = {
        'Gender': 'Gênero',
        'Age': 'Idade',
        'Height': 'Altura (m)',
        'Weight': 'Peso (kg)',
        'family_history': 'Histórico Familiar',
        'FAVC': 'Alimentos Altamente Calóricos',
        'FCVC': 'Frequência de Consumo de Vegetais',
        'NCP': 'Número de Refeições Principais',
        'CAEC': 'Come Entre Refeições',
        'SMOKE': 'Fuma',
        'CH2O': 'Consumo de Água',
        'SCC': 'Monitora Calorias',
        'FAF': 'Frequência de Atividade Física',
        'TUE': 'Tempo Usando Dispositivos Eletrônicos',
        'CALC': 'Frequência de Consumo de Álcool',
        'MTRANS': 'Meio de Transporte'
    }
    
    patient_data = []
    for key, value in input_data.items():
        # Traduzir nome do campo
        field_name = field_translations.get(key, key.replace('_', ' ').title())
        
        # Traduzir valores
        if key in TRANSLATIONS and value in TRANSLATIONS[key]:
            value = TRANSLATIONS[key][value]
        
        patient_data.append([field_name, str(value)])
    
    patient_table = Table(patient_data, colWidths=[2.5*inch, 3.5*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(patient_table)
    
    # Rodapé
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "<i>Sistema desenvolvido para o Tech Challenge 4 - FIAP | Uso exclusivo para fins educacionais</i>",
        styles['Normal']
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# Menu lateral
with st.sidebar:
    # Logo/Título estilizado
    st.markdown("""
    <div class="logo-title">
        🏥 Sistema Preditivo<br>de Obesidade
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Início", "Predição de Obesidade", "Insights e Métricas"],
        icons=["house", "activity", "graph-up"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "transparent"},
            "icon": {"color": "#1e293b", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "color": "#1e293b",
                "background-color": "transparent",
                "--hover-color": "#b3d9f2",
                "border-radius": "5px",
                "font-weight": "500",
            },
            "nav-link-selected": {
                "background-color": "rgba(0, 92, 169, 0.9)",
                "color": "#ffffff",
                "font-weight": "600",
            },
        }
    )
    
    st.markdown("---")
    
    # Seção Sobre o Sistema
    st.markdown("### ℹ️ Sobre o Sistema")
    st.markdown("""
    Este sistema foi desenvolvido como parte do Tech Challenge 4.
    
    **Funcionalidades:**
    - Predição do nível de obesidade
    - Análise de probabilidades por classe
    - Dashboard com insights analíticos
    - Recomendações baseadas nos dados
    
    **Modelo:**
    - Algoritmo: Random Forest
    - Acurácia: 98.58%
    
    Desenvolvido para auxiliar profissionais de saúde
    """)

# Página Início
if selected == "Início":
    st.title("🏥 Bem-vindo ao Sistema Preditivo de Obesidade")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Objetivo
        
        Este sistema utiliza Machine Learning para auxiliar médicos e médicas na previsão do nível de obesidade de pacientes, 
        fornecendo ferramentas para auxiliar na tomada de decisão clínica.
        """)
        
        st.markdown("""
        ### 🔮 Predição
        
        Na aba **Predição de Obesidade**, você pode:
        
        - Preencher dados do paciente
        - Obter predição do nível de obesidade
        - Ver probabilidades por classe
        - Receber recomendações personalizadas
        - Exportar relatório em PDF
        """)
        
        st.markdown("""
        ### 📊 Insights e Métricas
        
        Na aba **Insights e Métricas**, você encontra:
        
        - Visualizações interativas dos dados
        - Análises e insights sobre obesidade
        - Métricas do modelo
        - Recomendações clínicas
        """)
    
    with col2:
        st.markdown("### 📈 Recursos")
        st.info("""
        - Modelo com 98.58% de acurácia
        - Interface intuitiva e profissional
        - Análises baseadas em dados reais
        """)
        
        st.markdown("### 🚀 Como Usar")
        st.markdown("""
        **Para fazer uma predição:**
        
        1. Navegue para a aba "🔮 Predição de Obesidade"
        2. Preencha o formulário com os dados do paciente
        3. Clique em "Fazer Predição"
        4. Analise os resultados e recomendações
        5. Exporte o relatório em PDF se necessário
        
        **Para análise de dados:**
        
        1. Navegue para a aba "📊 Insights e Métricas"
        2. Explore os gráficos e insights apresentados
        3. Analise as métricas do modelo
        """)
    
    st.markdown("---")
    
    # Métricas principais
    st.markdown("### 📋 Informações Técnicas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Acurácia do Modelo", "98.58%")
    
    with col2:
        st.metric("Total de Registros", "2.111")
    
    with col3:
        st.metric("Variáveis de Entrada", "16")
    
    with col4:
        st.metric("Classes de Obesidade", "7")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 2rem;'>
        <p>Sistema desenvolvido para o Tech Challenge 4 - FIAP | Uso exclusivo para fins educacionais</p>
    </div>
    """, unsafe_allow_html=True)

# Página Predição
elif selected == "Predição de Obesidade":
    st.title("🔮 Predição de Nível de Obesidade")
    st.markdown("---")
    
    # Carregar modelo
    model, preprocessor_data = load_model()
    
    if model is None or preprocessor_data is None:
        st.error("Não foi possível carregar o modelo. Verifique se os arquivos estão no diretório correto.")
        st.stop()
    
    # Seção de informações do médico e paciente
    st.subheader("👨‍⚕️ Informações do Profissional e Paciente")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        medico_nome = st.text_input("Nome do Profissional (opcional)", placeholder="Ex: Dr. João Silva")
    
    with col2:
        medico_crm = st.text_input("Registro do Conselho (opcional)", placeholder="Ex: CRM 123456")
    
    with col3:
        paciente_nome = st.text_input("Nome do Paciente (opcional)", placeholder="Ex: Maria Santos")
    
    st.markdown("---")
    
    # Formulário de entrada - Reorganizado para melhor uso do espaço
    st.subheader("📝 Dados do Paciente")
    
    # Primeira linha: Dados Demográficos em 3 colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 Dados Demográficos")
        gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
        age = st.number_input("Idade", min_value=1, max_value=120, value=30)
    
    with col2:
        st.markdown("#### 📏 Medidas")
        height = st.number_input("Altura (metros)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
        weight = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.1)
        
        # Calcular IMC
        if height > 0:
            bmi = weight / (height ** 2)
            st.info(f"**IMC:** {bmi:.2f}")
    
    with col3:
        st.markdown("#### 👨‍👩‍👧‍👦 Histórico")
        family_history = st.selectbox("Histórico familiar de excesso de peso", ["Sim", "Não"])
    
    st.markdown("---")
    
    # Segunda linha: Hábitos Alimentares em 3 colunas
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("#### 🍽️ Alimentação")
        favc = st.selectbox("Alimentos altamente calóricos?", ["Sim", "Não"])
        fcvc = st.number_input("Frequência de consumo de vegetais (1-3): 1=raramente, 2=às vezes, 3=sempre", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
        ncp = st.number_input("Número de refeições principais (1-4): 1=uma, 2=duas, 3=três, 4=quatro ou mais", min_value=1.0, max_value=4.0, value=3.0, step=0.1)
    
    with col5:
        st.markdown("#### 💧 Hidratação")
        caec = st.selectbox("Come entre refeições?", ["Não", "Às vezes", "Frequentemente", "Sempre"])
        ch2o = st.number_input("Consumo diário de água (1-3): 1=<1L/dia, 2=1-2L/dia, 3=>2L/dia", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
        scc = st.selectbox("Monitora ingestão calórica diária?", ["Sim", "Não"])
    
    with col6:
        st.markdown("#### 🏃 Estilo de Vida")
        smoke = st.selectbox("Fuma?", ["Sim", "Não"])
        faf = st.number_input("Frequência semanal de atividade física (0-3): 0=nenhuma, 1=1-2×/sem, 2=3-4×/sem, 3=5×/sem ou mais", min_value=0.0, max_value=3.0, value=1.0, step=0.1)
        tue = st.number_input("Tempo diário usando dispositivos eletrônicos (0-2): 0=0-2h/dia, 1=3-5h/dia, 2=>5h/dia", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
    
    st.markdown("---")
    
    # Terceira linha: Outros hábitos
    col7, col8 = st.columns(2)
    
    with col7:
        calc = st.selectbox("Frequência de consumo de álcool", ["Não", "Às vezes", "Frequentemente", "Sempre"])
    
    with col8:
        mtrans = st.selectbox("Meio de transporte", [
            "Transporte Público",
            "Automóvel",
            "Caminhada",
            "Motocicleta",
            "Bicicleta"
        ])
    
    # Converter valores para inglês (formato do modelo)
    gender_en = "Male" if gender == "Masculino" else "Female"
    family_history_en = "yes" if family_history == "Sim" else "no"
    favc_en = "yes" if favc == "Sim" else "no"
    smoke_en = "yes" if smoke == "Sim" else "no"
    scc_en = "yes" if scc == "Sim" else "no"
    
    caec_map = {"Não": "no", "Às vezes": "Sometimes", "Frequentemente": "Frequently", "Sempre": "Always"}
    caec_en = caec_map[caec]
    
    calc_map = {"Não": "no", "Às vezes": "Sometimes", "Frequentemente": "Frequently", "Sempre": "Always"}
    calc_en = calc_map[calc]
    
    mtrans_map = {
        "Transporte Público": "Public_Transportation",
        "Automóvel": "Automobile",
        "Caminhada": "Walking",
        "Motocicleta": "Motorbike",
        "Bicicleta": "Bike"
    }
    mtrans_en = mtrans_map[mtrans]
    
    # Arredondar valores decimais para inteiros conforme dicionário
    fcvc_rounded = round(fcvc)
    ncp_rounded = round(ncp)
    ch2o_rounded = round(ch2o)
    faf_rounded = round(faf)
    tue_rounded = round(tue)
    
    input_data = {
        'Gender': gender_en,
        'Age': age,
        'Height': height,
        'Weight': weight,
        'family_history': family_history_en,
        'FAVC': favc_en,
        'FCVC': fcvc_rounded,
        'NCP': ncp_rounded,
        'CAEC': caec_en,
        'SMOKE': smoke_en,
        'CH2O': ch2o_rounded,
        'SCC': scc_en,
        'FAF': faf_rounded,
        'TUE': tue_rounded,
        'CALC': calc_en,
        'MTRANS': mtrans_en
    }
    
    # Botão de predição
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        predict_button = st.button("🔮 Fazer Predição", type="primary", use_container_width=True)
    
    # Fazer predição
    if predict_button:
        with st.spinner("Processando predição..."):
            prediction, probabilities, classes = make_prediction(input_data, model, preprocessor_data)
        
        if prediction is not None:
            st.markdown("---")
            st.header("📊 Resultado da Predição")
            
            # Resultado principal
            prediction_pt = OBESITY_LEVELS_PT.get(prediction, prediction)
            
            # Container para resultado
            st.markdown(f"""
            <div class="result-box">
                <h2 style="color: white; margin: 0;">🎯 Nível de Obesidade Previsto</h2>
                <h1 style="color: white; margin: 1rem 0;">{prediction_pt}</h1>
            </div>
            """, unsafe_allow_html=True)
            
            # Probabilidade da classe predita
            pred_idx = list(classes).index(prediction)
            confidence = probabilities[pred_idx] * 100
            st.progress(confidence / 100)
            st.caption(f"**Confiança:** {confidence:.2f}%")
            
            # Probabilidades por classe
            st.markdown("---")
            st.subheader("📈 Probabilidades por Classe")
            
            # Criar DataFrame com probabilidades
            prob_df = pd.DataFrame({
                'Nível de Obesidade': [OBESITY_LEVELS_PT.get(c, c) for c in classes],
                'Probabilidade (%)': [p * 100 for p in probabilities]
            }).sort_values('Probabilidade (%)', ascending=False)
            
            # Gráfico de barras
            fig = px.bar(
                prob_df,
                x='Nível de Obesidade',
                y='Probabilidade (%)',
                color='Probabilidade (%)',
                color_continuous_scale='Blues',
                title='Probabilidades por Nível de Obesidade'
            )
            fig.update_layout(
                xaxis_tickangle=-45,
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela
            st.dataframe(prob_df, use_container_width=True, hide_index=True)
            
            # Recomendações
            st.markdown("---")
            st.subheader("💡 Recomendações")
            
            if 'Obesity' in prediction or 'Overweight' in prediction:
                st.warning("""
                **⚠️ Atenção:** O modelo indica risco de sobrepeso/obesidade. Recomenda-se:
                - Consultar um profissional de saúde
                - Avaliar hábitos alimentares
                - Aumentar atividade física regular
                - Monitorar peso e IMC periodicamente
                """)
            elif prediction == 'Normal_Weight':
                st.success("""
                **✅ Peso Normal:** Mantenha hábitos saudáveis:
                - Continue com alimentação balanceada
                - Mantenha atividade física regular
                - Monitore peso periodicamente
                """)
            else:
                st.info("""
                **ℹ️ Peso Insuficiente:** Consulte um nutricionista para:
                - Avaliar necessidades nutricionais
                - Desenvolver plano alimentar adequado
                - Monitorar ganho de peso saudável
                """)
            
            # Exportar PDF
            st.markdown("---")
            st.subheader("📄 Exportar Relatório")
            
            pdf_buffer = generate_pdf(medico_nome, medico_crm, paciente_nome, input_data, prediction, probabilities, classes)
            
            # Nome do arquivo PDF
            if paciente_nome and paciente_nome.strip():
                file_name = f"relatorio_obesidade_{paciente_nome.strip().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            else:
                file_name = f"relatorio_obesidade_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            st.download_button(
                label="📥 Baixar Relatório em PDF",
                data=pdf_buffer,
                file_name=file_name,
                mime="application/pdf",
                type="primary"
            )

# Página Insights e Métricas
elif selected == "Insights e Métricas":
    st.title("📊 Insights e Métricas")
    st.markdown("---")
    st.markdown("""
    Este dashboard apresenta insights e análises sobre os dados de obesidade para auxiliar a equipe médica na tomada de decisão.
    """)
    
    # Carregar dados
    @st.cache_data
    def load_data():
        """Carrega os dados"""
        try:
            df = pd.read_csv('data/obesity.csv')
            # Criar IMC
            df['BMI'] = df['Weight'] / (df['Height'] ** 2)
            return df
        except FileNotFoundError:
            st.error("Arquivo de dados não encontrado. Execute primeiro o script de extração.")
            return None
    
    df = load_data()
    
    if df is not None:
        # Filtros no topo da página
        st.header("🔍 Filtros", anchor="filtros")
        
        # Container para filtros
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            # Filtro por gênero - usando checkboxes igual ao de obesidade
            st.markdown('<p style="color: #2c3e50; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem;">Gênero</p>', unsafe_allow_html=True)
            
            gender_options_en = df['Gender'].unique()
            gender_options_pt = ['Masculino' if g == 'Male' else 'Feminino' for g in gender_options_en]
            gender_mapping = dict(zip(gender_options_pt, gender_options_en))
            
            # Inicializar session_state se necessário
            if 'gender_filters' not in st.session_state:
                st.session_state.gender_filters = {g: True for g in gender_options_pt}
            
            # Container para checkboxes (sem borda)
            st.markdown("""
            <div class="obesity-checkbox-container">
            """, unsafe_allow_html=True)
            
            gender_selected_pt = []
            for gender_pt in gender_options_pt:
                if gender_pt not in st.session_state.gender_filters:
                    st.session_state.gender_filters[gender_pt] = True
                
                checked = st.checkbox(
                    gender_pt,
                    value=st.session_state.gender_filters[gender_pt],
                    key=f"gender_{gender_pt}"
                )
                st.session_state.gender_filters[gender_pt] = checked
                
                if checked:
                    gender_selected_pt.append(gender_pt)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Se nenhum selecionado, selecionar todos
            if not gender_selected_pt:
                gender_selected_pt = gender_options_pt
                for gender_pt in gender_options_pt:
                    st.session_state.gender_filters[gender_pt] = True
            
            # Converter de volta para inglês para filtro
            gender_filter = [gender_mapping[g] for g in gender_selected_pt]
        
        with filter_col2:
            # Filtro por nível de obesidade - usando checkboxes para mostrar todos sem scroll
            st.markdown('<p style="color: #2c3e50; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem;">Nível de Obesidade</p>', unsafe_allow_html=True)
            
            obesity_options_en = df['Obesity'].unique()
            obesity_options_pt = [OBESITY_LEVELS_PT.get(obs, obs) for obs in obesity_options_en]
            obesity_mapping = dict(zip(obesity_options_pt, obesity_options_en))
            
            # Inicializar session_state se necessário
            if 'obesity_filters' not in st.session_state:
                st.session_state.obesity_filters = {obs: True for obs in obesity_options_pt}
            
            # Container para checkboxes (sem borda, sem background)
            # Não usar div com classe para evitar borda
            
            # Criar checkboxes
            obesity_selected_pt = []
            for obs_pt in obesity_options_pt:
                # Usar session_state para manter estado
                if obs_pt not in st.session_state.obesity_filters:
                    st.session_state.obesity_filters[obs_pt] = True
                
                checked = st.checkbox(
                    obs_pt,
                    value=st.session_state.obesity_filters[obs_pt],
                    key=f"obesity_{obs_pt}"
                )
                st.session_state.obesity_filters[obs_pt] = checked
                
                if checked:
                    obesity_selected_pt.append(obs_pt)
            
            # Se nenhum selecionado, selecionar todos (evitar lista vazia)
            if not obesity_selected_pt:
                obesity_selected_pt = obesity_options_pt
                # Atualizar session_state
                for obs_pt in obesity_options_pt:
                    st.session_state.obesity_filters[obs_pt] = True
            
            # Converter de volta para inglês para filtro
            obesity_filter = [obesity_mapping[obs] for obs in obesity_selected_pt]
        
        with filter_col3:
            # Filtro por idade
            age_range = st.slider(
                "Faixa Etária (anos)",
                min_value=int(df['Age'].min()),
                max_value=int(df['Age'].max()),
                value=(int(df['Age'].min()), int(df['Age'].max()))
            )
        
        st.markdown("---")
        
        # Aplicar filtros
        df_filtered = df[
            (df['Gender'].isin(gender_filter)) &
            (df['Obesity'].isin(obesity_filter)) &
            (df['Age'] >= age_range[0]) &
            (df['Age'] <= age_range[1])
        ]
        
        # Mostrar quantidade de registros filtrados
        if len(df_filtered) < len(df):
            st.info(f"📊 Mostrando {len(df_filtered)} de {len(df)} registros com os filtros aplicados.")
        
        st.markdown("---")
        
        # Métricas principais
        st.header("📈 Métricas Principais")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Registros", len(df_filtered), delta=None)
        
        with col2:
            avg_bmi = df_filtered['BMI'].mean()
            st.metric("IMC Médio", f"{avg_bmi:.2f}")
        
        with col3:
            avg_age = df_filtered['Age'].mean()
            st.metric("Idade Média", f"{avg_age:.1f} anos")
        
        with col4:
            obesity_rate = (df_filtered['Obesity'].str.contains('Obesity|Overweight').sum() / len(df_filtered)) * 100
            st.metric("Taxa de Sobrepeso/Obesidade", f"{obesity_rate:.1f}%")
        
        st.markdown("---")
        
        # Distribuição de Obesidade
        st.header("📊 Distribuição de Níveis de Obesidade")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de barras
            obesity_counts = df_filtered['Obesity'].value_counts()
            # Traduzir labels
            obesity_counts_pt = pd.Series({
                OBESITY_LEVELS_PT.get(k, k): v for k, v in obesity_counts.items()
            })
            
            fig_bar = px.bar(
                x=obesity_counts_pt.index,
                y=obesity_counts_pt.values,
                labels={'x': 'Nível de Obesidade', 'y': 'Frequência'},
                title='Distribuição de Níveis de Obesidade',
                color=obesity_counts_pt.values,
                color_continuous_scale='Blues'
            )
            fig_bar.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Gráfico de pizza
            fig_pie = px.pie(
                values=obesity_counts.values,
                names=[OBESITY_LEVELS_PT.get(k, k) for k in obesity_counts.index],
                title='Proporção de Níveis de Obesidade',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        
        # Análise por Gênero
        st.header("👥 Análise por Gênero")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender_obesity = pd.crosstab(df_filtered['Gender'], df_filtered['Obesity'])
            # Traduzir colunas
            gender_obesity.columns = [OBESITY_LEVELS_PT.get(col, col) for col in gender_obesity.columns]
            gender_obesity.index = ['Feminino' if idx == 'Female' else 'Masculino' for idx in gender_obesity.index]
            
            fig_gender = px.bar(
                gender_obesity,
                barmode='group',
                title='Distribuição de Obesidade por Gênero',
                labels={'value': 'Frequência', 'Gender': 'Gênero'},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_gender.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_gender, use_container_width=True)
        
        with col2:
            avg_bmi_gender = df_filtered.groupby('Gender')['BMI'].mean()
            avg_bmi_gender.index = ['Feminino' if idx == 'Female' else 'Masculino' for idx in avg_bmi_gender.index]
            
            fig_bmi_gender = px.bar(
                x=avg_bmi_gender.index,
                y=avg_bmi_gender.values,
                title='IMC Médio por Gênero',
                labels={'x': 'Gênero', 'y': 'IMC Médio'},
                color=avg_bmi_gender.values,
                color_continuous_scale='Oranges'
            )
            fig_bmi_gender.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_bmi_gender, use_container_width=True)
        
        st.markdown("---")
        
        # Análise por Idade
        st.header("📅 Análise por Idade")
        
        # Criar faixas etárias
        df_filtered['Faixa Etária'] = pd.cut(
            df_filtered['Age'],
            bins=[0, 20, 30, 40, 50, 100],
            labels=['<20', '20-30', '30-40', '40-50', '50+']
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            age_obesity = pd.crosstab(df_filtered['Faixa Etária'], df_filtered['Obesity'])
            age_obesity.columns = [OBESITY_LEVELS_PT.get(col, col) for col in age_obesity.columns]
            
            fig_age = px.bar(
                age_obesity,
                barmode='group',
                title='Distribuição de Obesidade por Faixa Etária',
                labels={'value': 'Frequência', 'Faixa Etária': 'Faixa Etária'},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_age.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_age, use_container_width=True)
        
        with col2:
            # Scatter plot: Idade vs IMC
            df_filtered_plot = df_filtered.copy()
            df_filtered_plot['Obesity_PT'] = df_filtered_plot['Obesity'].map(OBESITY_LEVELS_PT)
            
            fig_scatter = px.scatter(
                df_filtered_plot,
                x='Age',
                y='BMI',
                color='Obesity_PT',
                title='Relação entre Idade e IMC',
                labels={'Age': 'Idade', 'BMI': 'IMC'},
                hover_data=['Gender', 'Weight', 'Height'],
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_scatter.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown("---")
        
        # Análise de Hábitos
        st.header("🍽️ Análise de Hábitos e Estilo de Vida")
        
        try:
            # Atividade Física
            col1, col2 = st.columns(2)
            
            with col1:
                # Arredondar FAF para valores inteiros (0, 1, 2, 3) para evitar muitas barras
                df_faf_rounded = df_filtered.copy()
                df_faf_rounded['FAF_rounded'] = df_faf_rounded['FAF'].round().astype(int).clip(0, 3)
                
                # Criar crosstab com valores arredondados
                faf_obesity = pd.crosstab(df_faf_rounded['FAF_rounded'], df_faf_rounded['Obesity'])
                faf_obesity.columns = [OBESITY_LEVELS_PT.get(col, col) for col in faf_obesity.columns]
                
                # Calcular percentuais para melhor visualização
                faf_obesity_pct = faf_obesity.div(faf_obesity.sum(axis=1), axis=0) * 100
                
                # Mapear níveis de atividade física para labels descritivos
                faf_labels = {
                    0: 'Nenhuma (0)',
                    1: 'Baixa (1-2×/sem)',
                    2: 'Moderada (3-4×/sem)',
                    3: 'Alta (5+×/sem)'
                }
                faf_obesity_pct.index = [faf_labels.get(idx, f'{idx}') for idx in faf_obesity_pct.index]
                
                # Reordenar colunas para ordem lógica (do mais saudável ao menos saudável)
                ordem_colunas = ['Peso Insuficiente', 'Peso Normal', 'Sobrepeso Nível I', 
                                'Sobrepeso Nível II', 'Obesidade Tipo I', 'Obesidade Tipo II', 'Obesidade Tipo III']
                ordem_colunas = [col for col in ordem_colunas if col in faf_obesity_pct.columns]
                faf_obesity_pct = faf_obesity_pct[ordem_colunas]
                
                # Criar gráfico de barras empilhadas com percentuais (otimizado)
                fig_faf = px.bar(
                    faf_obesity_pct,
                    barmode='stack',
                    title='📊 Impacto da Atividade Física na Obesidade',
                    labels={
                        'value': 'Percentual (%)',
                        'index': 'Frequência de Atividade Física',
                        'variable': 'Nível de Obesidade'
                    },
                    color_discrete_sequence=[
                        '#10b981',  # Verde - Peso Insuficiente
                        '#3b82f6',  # Azul - Peso Normal
                        '#f59e0b',  # Amarelo - Sobrepeso I
                        '#f97316',  # Laranja - Sobrepeso II
                        '#ef4444',  # Vermelho claro - Obesidade I
                        '#dc2626',  # Vermelho - Obesidade II
                        '#991b1b'   # Vermelho escuro - Obesidade III
                    ]
                )
                
                fig_faf.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=0,
                    height=500,
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=1,
                        xanchor="left",
                        x=1.02,
                        title_text="Nível de Obesidade",
                        font=dict(size=10),
                        bgcolor='rgba(255,255,255,0.8)',
                        bordercolor='rgba(0,0,0,0.2)',
                        borderwidth=1
                    ),
                    xaxis=dict(
                        title='Frequência de Atividade Física', 
                        title_font=dict(size=12),
                        tickmode='linear',
                        tick0=0,
                        dtick=1
                    ),
                    yaxis=dict(
                        title='Percentual (%)', 
                        title_font=dict(size=12),
                        range=[0, 100],  # FORÇAR limite de 0 a 100%
                        tickmode='linear',
                        tick0=0,
                        dtick=20
                    ),
                    title_font=dict(size=16, color='#1e293b'),
                    hovermode='x unified',
                    bargap=0.3  # Espaçamento entre barras para melhor visualização
                )
                
                # Atualizar hovertemplate para mostrar percentuais
                for trace in fig_faf.data:
                    trace.hovertemplate = '<b>%{fullData.name}</b><br>' + \
                                         'Frequência de Atividade Física: %{x}<br>' + \
                                         'Percentual: %{y:.1f}%<br>' + \
                                         '<extra></extra>'
                
                st.plotly_chart(fig_faf, use_container_width=True)
                
                # Adicionar insights abaixo do gráfico
                st.caption("💡 **Insight:** Quanto maior a frequência de atividade física, menor a proporção de casos de obesidade.")
        
            with col2:
                # Histórico familiar
                family_obesity = pd.crosstab(df_filtered['family_history'], df_filtered['Obesity'])
                family_obesity.columns = [OBESITY_LEVELS_PT.get(col, col) for col in family_obesity.columns]
                family_obesity.index = ['Sim' if idx == 'yes' else 'Não' for idx in family_obesity.index]
                
                fig_family = px.bar(
                    family_obesity,
                    barmode='group',
                    title='Impacto do Histórico Familiar',
                    labels={'value': 'Frequência', 'family_history': 'Histórico Familiar'},
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_family.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_family, use_container_width=True)
            
            # Consumo de alimentos calóricos
            col3, col4 = st.columns(2)
            
            with col3:
                favc_obesity = pd.crosstab(df_filtered['FAVC'], df_filtered['Obesity'])
                favc_obesity.columns = [OBESITY_LEVELS_PT.get(col, col) for col in favc_obesity.columns]
                favc_obesity.index = ['Sim' if idx == 'yes' else 'Não' for idx in favc_obesity.index]
                
                fig_favc = px.bar(
                    favc_obesity,
                    barmode='group',
                    title='Impacto de Alimentos Altamente Calóricos',
                    labels={'value': 'Frequência', 'FAVC': 'Alimentos Calóricos'},
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_favc.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_favc, use_container_width=True)
            
            with col4:
                # Consumo de vegetais
                fcvc_obesity = df_filtered.groupby('Obesity')['FCVC'].mean()
                fcvc_obesity.index = [OBESITY_LEVELS_PT.get(idx, idx) for idx in fcvc_obesity.index]
                
                fig_fcvc = px.bar(
                    x=fcvc_obesity.index,
                    y=fcvc_obesity.values,
                    title='Consumo Médio de Vegetais por Nível de Obesidade',
                    labels={'x': 'Nível de Obesidade', 'y': 'Consumo Médio de Vegetais'},
                    color=fcvc_obesity.values,
                    color_continuous_scale='Greens'
                )
                fig_fcvc.update_layout(
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_fcvc, use_container_width=True)
        
        except Exception as e:
            st.error(f"Erro ao gerar gráficos de hábitos e estilo de vida: {str(e)}")
            st.info("Tente recarregar a página ou ajustar os filtros.")
        
        st.markdown("---")
        
        # Análise de Correlação
        st.header("🔗 Análise de Correlação")
        st.markdown("""
        Esta seção apresenta a análise de correlação entre as variáveis numéricas e suas relações com o nível de obesidade.
        """)
        
        # Preparar dados numéricos para correlação
        numerical_cols = ['Age', 'Height', 'Weight', 'BMI', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
        numerical_cols = [col for col in numerical_cols if col in df_filtered.columns]
        
        if len(numerical_cols) > 0:
            corr_df = df_filtered[numerical_cols].corr()
            
            # Heatmap de correlação
            fig_corr = go.Figure(data=go.Heatmap(
                z=corr_df.values,
                x=corr_df.columns,
                y=corr_df.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_df.round(2).values,
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Correlação")
            ))
            fig_corr.update_layout(
                title='Matriz de Correlação entre Variáveis Numéricas',
                height=600,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Análise de correlações específicas
            st.subheader("📊 Correlações com IMC e Obesidade")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Correlação IMC vs outras variáveis
                if 'BMI' in corr_df.columns:
                    bmi_corr = corr_df['BMI'].sort_values(ascending=False)
                    bmi_corr = bmi_corr[bmi_corr.index != 'BMI']
                    
                    fig_bmi_corr = px.bar(
                        x=bmi_corr.values,
                        y=bmi_corr.index,
                        orientation='h',
                        title='Correlação das Variáveis com IMC',
                        labels={'x': 'Correlação', 'y': 'Variável'},
                        color=bmi_corr.values,
                        color_continuous_scale='RdYlGn',
                        color_continuous_midpoint=0
                    )
                    fig_bmi_corr.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig_bmi_corr, use_container_width=True)
            
            with col2:
                # Tabela de correlações
                st.markdown("**Principais Correlações:**")
                corr_table = []
                for col in numerical_cols:
                    if col != 'BMI' and 'BMI' in corr_df.columns:
                        corr_val = corr_df.loc[col, 'BMI']
                        corr_table.append({
                            'Variável': col,
                            'Correlação com IMC': f"{corr_val:.3f}",
                            'Interpretação': 'Forte' if abs(corr_val) > 0.7 else 'Moderada' if abs(corr_val) > 0.4 else 'Fraca'
                        })
                
                if corr_table:
                    corr_table_df = pd.DataFrame(corr_table).sort_values('Correlação com IMC', key=lambda x: x.str.replace('Correlação com IMC', '').astype(float).abs(), ascending=False)
                    st.dataframe(corr_table_df, use_container_width=True, hide_index=True)
        
        # Conclusão da Análise de Correlação
        with st.expander("📝 Conclusão da Análise de Correlação", expanded=False):
            st.markdown("""
            **Principais Descobertas:**
            
            1. **IMC e Peso/Altura:** Como esperado, há forte correlação positiva entre IMC e Peso, e negativa com Altura.
            
            2. **Atividade Física:** A frequência de atividade física (FAF) geralmente apresenta correlação negativa com IMC, indicando que maior atividade física está associada a menor IMC.
            
            3. **Hábitos Alimentares:** Variáveis como consumo de vegetais (FCVC) e número de refeições (NCP) podem apresentar correlações interessantes com o IMC.
            
            4. **Idade:** A correlação entre idade e IMC pode variar, mas geralmente há uma relação positiva moderada.
            
            **Implicações Clínicas:**
            - Variáveis com alta correlação com IMC são importantes preditores
            - Correlações moderadas podem indicar fatores de risco ou proteção
            - A análise de correlação ajuda a identificar variáveis redundantes ou complementares
            """)
        
        st.markdown("---")
        
        # Análise de Boxplots
        st.header("📦 Análise de Boxplots")
        st.markdown("""
        Os boxplots mostram a distribuição das variáveis numéricas por nível de obesidade, permitindo identificar diferenças, outliers e padrões.
        """)
        
        # Boxplots por nível de obesidade
        boxplot_vars = ['Age', 'BMI', 'Weight', 'Height', 'FAF', 'FCVC']
        boxplot_vars = [var for var in boxplot_vars if var in df_filtered.columns]
        
        if len(boxplot_vars) > 0:
            # Selecionar variáveis para boxplot
            selected_boxplot_vars = st.multiselect(
                "Selecione as variáveis para análise de boxplot:",
                options=boxplot_vars,
                default=boxplot_vars[:4] if len(boxplot_vars) >= 4 else boxplot_vars
            )
            
            if selected_boxplot_vars:
                # Criar boxplots
                num_vars = len(selected_boxplot_vars)
                cols_per_row = 2
                num_rows = (num_vars + cols_per_row - 1) // cols_per_row
                
                for i in range(0, num_vars, cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, var in enumerate(selected_boxplot_vars[i:i+cols_per_row]):
                        with cols[j]:
                            df_plot = df_filtered.copy()
                            df_plot['Obesity_PT'] = df_plot['Obesity'].map(OBESITY_LEVELS_PT)
                            
                            fig_box = px.box(
                                df_plot,
                                x='Obesity_PT',
                                y=var,
                                title=f'Distribuição de {var} por Nível de Obesidade',
                                color='Obesity_PT',
                                color_discrete_sequence=px.colors.qualitative.Set3
                            )
                            fig_box.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                xaxis_tickangle=-45,
                                showlegend=False,
                                height=400
                            )
                            st.plotly_chart(fig_box, use_container_width=True)
        
        # Conclusão da Análise de Boxplots
        with st.expander("📝 Conclusão da Análise de Boxplots", expanded=False):
            st.markdown("""
            **Principais Observações:**
            
            1. **Distribuição de IMC:** Os boxplots mostram claramente a separação entre diferentes níveis de obesidade, com medianas crescentes conforme o nível aumenta.
            
            2. **Outliers:** A presença de outliers pode indicar casos extremos que requerem atenção especial ou podem ser erros de medição.
            
            3. **Variabilidade:** A amplitude interquartil (IQR) mostra a variabilidade dentro de cada grupo. Grupos com maior IQR têm mais variabilidade.
            
            4. **Diferenças entre Grupos:** Boxplots permitem identificar visualmente diferenças significativas entre os níveis de obesidade para cada variável.
            
            5. **Idade e Outras Variáveis:** A distribuição da idade e outras características pode variar entre os grupos, indicando perfis diferentes.
            
            **Implicações:**
            - Identificação de grupos de risco com características distintas
            - Detecção de outliers que podem necessitar investigação adicional
            - Compreensão da variabilidade dentro de cada categoria de obesidade
            """)
        
        st.markdown("---")
        
        # Análise de Distribuição
        st.header("📊 Análise de Distribuição")
        st.markdown("""
        Esta seção apresenta análises detalhadas das distribuições das variáveis, incluindo histogramas, densidade e estatísticas descritivas.
        """)
        
        # Selecionar variáveis para análise de distribuição
        dist_vars = ['Age', 'BMI', 'Weight', 'Height', 'FAF', 'FCVC', 'NCP', 'CH2O', 'TUE']
        dist_vars = [var for var in dist_vars if var in df_filtered.columns]
        
        if len(dist_vars) > 0:
            selected_dist_var = st.selectbox(
                "Selecione a variável para análise de distribuição:",
                options=dist_vars
            )
            
            if selected_dist_var:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Histograma
                    fig_hist = px.histogram(
                        df_filtered,
                        x=selected_dist_var,
                        nbins=30,
                        title=f'Distribuição de {selected_dist_var}',
                        labels={selected_dist_var: selected_dist_var, 'count': 'Frequência'},
                        color_discrete_sequence=['#4CAF50']
                    )
                    fig_hist.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col2:
                    # Distribuição por nível de obesidade
                    df_plot = df_filtered.copy()
                    df_plot['Obesity_PT'] = df_plot['Obesity'].map(OBESITY_LEVELS_PT)
                    
                    fig_dist = px.histogram(
                        df_plot,
                        x=selected_dist_var,
                        color='Obesity_PT',
                        nbins=30,
                        title=f'Distribuição de {selected_dist_var} por Nível de Obesidade',
                        labels={selected_dist_var: selected_dist_var, 'count': 'Frequência'},
                        barmode='overlay',
                        opacity=0.7
                    )
                    fig_dist.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig_dist, use_container_width=True)
                
                # Estatísticas descritivas
                st.subheader(f"📈 Estatísticas Descritivas - {selected_dist_var}")
                
                stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                
                with stats_col1:
                    st.metric("Média", f"{df_filtered[selected_dist_var].mean():.2f}")
                
                with stats_col2:
                    st.metric("Mediana", f"{df_filtered[selected_dist_var].median():.2f}")
                
                with stats_col3:
                    st.metric("Desvio Padrão", f"{df_filtered[selected_dist_var].std():.2f}")
                
                with stats_col4:
                    st.metric("Coef. Variação", f"{(df_filtered[selected_dist_var].std() / df_filtered[selected_dist_var].mean() * 100):.2f}%")
                
                # Estatísticas por nível de obesidade
                st.subheader(f"📊 Estatísticas por Nível de Obesidade - {selected_dist_var}")
                
                stats_by_obesity = df_filtered.groupby('Obesity')[selected_dist_var].agg(['mean', 'median', 'std', 'min', 'max']).round(2)
                stats_by_obesity.index = [OBESITY_LEVELS_PT.get(idx, idx) for idx in stats_by_obesity.index]
                stats_by_obesity.columns = ['Média', 'Mediana', 'Desvio Padrão', 'Mínimo', 'Máximo']
                st.dataframe(stats_by_obesity, use_container_width=True)
        
        # Conclusão da Análise de Distribuição
        with st.expander("📝 Conclusão da Análise de Distribuição", expanded=False):
            st.markdown("""
            **Principais Descobertas:**
            
            1. **Normalidade:** A análise de distribuição permite verificar se as variáveis seguem distribuição normal, o que é importante para alguns testes estatísticos.
            
            2. **Assimetria:** Distribuições assimétricas podem indicar que a maioria dos valores está concentrada em uma faixa específica.
            
            3. **Diferenças entre Grupos:** As distribuições por nível de obesidade mostram como cada variável se comporta em diferentes categorias.
            
            4. **Valores Extremos:** A identificação de valores extremos (mínimos e máximos) ajuda a entender a amplitude dos dados.
            
            5. **Variabilidade:** O coeficiente de variação indica a variabilidade relativa dos dados, útil para comparar variáveis com escalas diferentes.
            
            **Implicações:**
            - Compreensão da natureza dos dados e suas características
            - Identificação de padrões e tendências
            - Base para decisões sobre transformações de dados se necessário
            - Suporte para interpretação de resultados do modelo
            """)
        
        st.markdown("---")
        
        # Insights e Recomendações
        st.header("💡 Insights e Recomendações")
        
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            st.subheader("🔍 Principais Descobertas")
            
            # Insight 1: Gênero
            gender_obesity_rate = df_filtered.groupby('Gender')['Obesity'].apply(
                lambda x: (x.str.contains('Obesity|Overweight').sum() / len(x)) * 100
            )
            dominant_gender = gender_obesity_rate.idxmax()
            dominant_gender_pt = 'Feminino' if dominant_gender == 'Female' else 'Masculino'
            
            st.info(f"""
            **Gênero mais afetado:** {dominant_gender_pt}
            - Taxa de sobrepeso/obesidade: {gender_obesity_rate[dominant_gender]:.1f}%
            """)
            
            # Insight 2: Atividade Física
            faf_impact = df_filtered.groupby('FAF')['Obesity'].apply(
                lambda x: (x.str.contains('Obesity|Overweight').sum() / len(x)) * 100
            )
            low_activity = (faf_impact.get(0.0, 0) + faf_impact.get(1.0, 0)) / 2 if (faf_impact.get(0.0, 0) + faf_impact.get(1.0, 0)) > 0 else 0
            high_activity = (faf_impact.get(2.0, 0) + faf_impact.get(3.0, 0)) / 2 if (faf_impact.get(2.0, 0) + faf_impact.get(3.0, 0)) > 0 else 0
            
            st.info(f"""
            **Atividade Física:**
            - Baixa atividade (0-1): {low_activity:.1f}% de sobrepeso/obesidade
            - Alta atividade (2-3): {high_activity:.1f}% de sobrepeso/obesidade
            """)
        
        with insights_col2:
            st.subheader("📋 Recomendações para Equipe Médica")
            
            st.success("""
            **1. Triagem Preventiva:**
            - Priorizar pacientes com histórico familiar
            - Monitorar pacientes com baixa atividade física
            
            **2. Intervenções:**
            - Programas de atividade física para grupos de risco
            - Educação nutricional sobre alimentos calóricos
            
            **3. Monitoramento:**
            - Acompanhamento regular de IMC
            - Avaliação de hábitos alimentares
            """)
        
        st.markdown("---")
        
        # Tabela de dados
        st.header("📋 Dados Filtrados")
        
        if st.checkbox("Mostrar dados completos"):
            st.dataframe(df_filtered, use_container_width=True, height=400)
        
        # Download dos dados
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download dos dados filtrados (CSV)",
            data=csv,
            file_name="obesity_filtered.csv",
            mime="text/csv"
        )
    
    else:
        st.error("Não foi possível carregar os dados. Verifique se o arquivo existe.")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 2rem;'>
        <p>Sistema desenvolvido para o Tech Challenge 4 - FIAP | Uso exclusivo para fins educacionais</p>
    </div>
    """, unsafe_allow_html=True)
