"""Normalización de la frase ingresada."""

import re


def tokenizar_frase(frase):
    texto = frase.strip().lower()
    texto = re.sub(r"[.!?]$", "", texto)
    return texto.split()