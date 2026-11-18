"""
Citizen Assist AI Mobilidade - Módulo de decisão lógica (Computer Science)
Programa interativo: o usuário informa as entradas e vê a orientação.

Execução:  python main.py
"""

import re
import sys

from logica_gratuidade import (AVISO, DATA_CONSULTA, FONTES, LIMITACOES, VARIAVEIS, g_simplificada,
                               m_simplificada, orientar)

SIM = {"s", "sim", "1", "y"}
NAO = {"n", "nao", "não", "0"}


class Sair(Exception):
    """Usuário encerrou a entrada (Ctrl+D / Ctrl+Z / Ctrl+C)."""


def ler(prompt: str) -> str:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        raise Sair()


def parece_dado_pessoal(texto: str) -> bool:
    """Bloqueia CPF, telefone, e-mail ou qualquer sequência de 8 ou mais dígitos."""
    return "@" in texto or len(re.sub(r"\D", "", texto)) >= 8


def aviso_dado_pessoal():
    print("  [!] Parece que você digitou um dado pessoal (CPF, telefone ou e-mail).")
    print("      Não informe dados pessoais: este assistente não precisa deles e nada foi registrado.")


def perguntar_sim_nao(letra: str) -> int:
    pergunta, significado = VARIAVEIS[letra]
    while True:
        resp = ler(f"\n{letra}) {pergunta}\n   [{significado}]\n   Responda s (sim) ou n (não): ").strip().lower()
        if parece_dado_pessoal(resp):
            aviso_dado_pessoal()
            continue
        if resp in SIM:
            return 1
        if resp in NAO:
            return 0
        if resp == "":
            print("  [!] Resposta vazia. Digite s para sim ou n para não.")
        else:
            print(f"  [!] \"{resp}\" não é uma resposta válida. Digite apenas s (sim) ou n (não).")


def mostrar_orientacao(A, B, C, D):
    o = orientar(A, B, C, D)
    print("\n" + "-" * 70)
    print(f"Entradas: A={A}  B={B}  C={C}  D={D}")
    print(f"Saídas:   G = A + B + C·D = {o.g}    |    M = C·G' = {o.m}")
    print("-" * 70)
    print(f">> {o.titulo}")
    for i, p in enumerate(o.passos, 1):
        print(f"\n{i}. {p}")
    print(f"\nFontes (consultadas em {DATA_CONSULTA}):")
    vistas = []
    for nome, url in o.fontes:
        if url not in vistas:
            vistas.append(url)
            print(f"  - {nome}\n    {url}")
    print(f"\nAVISO: {AVISO}")
    print("-" * 70)


def consulta_guiada():
    print("\nResponda 4 perguntas de sim ou não. Não pedimos idade exata, nome nem documentos.")
    valores = [perguntar_sim_nao(l) for l in "ABCD"]
    mostrar_orientacao(*valores)


def consulta_binaria():
    while True:
        cod = ler("\nDigite as 4 entradas ABCD como bits (ex.: 1010) ou v para voltar: ").strip().lower()
        if cod == "v":
            return
        if parece_dado_pessoal(cod):
            aviso_dado_pessoal()
            continue
        cod = cod.replace(" ", "")
        if len(cod) == 4 and set(cod) <= {"0", "1"}:
            mostrar_orientacao(*(int(c) for c in cod))
            return
        print("  [!] Entrada inválida. Use exatamente 4 dígitos, cada um 0 ou 1 (ex.: 0011).")


def tabela_verdade():
    print("\nTabela-verdade calculada pela lógica SIMPLIFICADA implementada:")
    print("  m | A B C D | G | M | Orientação")
    print("  --+---------+---+---+-------------------------")
    for i in range(16):
        A, B, C, D = (i >> 3) & 1, (i >> 2) & 1, (i >> 1) & 1, i & 1
        g, m = g_simplificada(A, B, C, D), m_simplificada(A, B, C, D)
        texto = "gratuidade" if g else ("meia tarifa" if m else "tarifa integral")
        print(f" {i:2d} | {A} {B} {C} {D} | {g} | {m} | {texto}")


def sobre():
    print("\nSOBRE ESTE MÓDULO")
    print("Variáveis:")
    for l, (p, s) in VARIAVEIS.items():
        print(f"  {l}: {p}\n     {s}")
    print("Saídas:\n  G: 1 = orientar gratuidade | 0 = sem gratuidade")
    print("  M: 1 = orientar meia tarifa de estudante | 0 = não se aplica")
    print("\nLimitações:")
    for l in LIMITACOES:
        print(f"  - {l}")
    print("\nFontes:")
    for nome, url in FONTES:
        print(f"  - {nome}\n    {url}")
    print(f"\n{AVISO}")


MENU = """
==================================================================
 CITIZEN ASSIST AI MOBILIDADE - Tenho direito a gratuidade no ônibus?
==================================================================
 1 - Consulta guiada (4 perguntas de sim/não)
 2 - Consulta rápida digitando os bits ABCD
 3 - Ver a tabela-verdade completa
 4 - Sobre: variáveis, fontes e limitações
 0 - Sair"""


def main():
    print(f"\n{AVISO}")
    acoes = {"1": consulta_guiada, "2": consulta_binaria, "3": tabela_verdade, "4": sobre}
    try:
        while True:
            print(MENU)
            op = ler("Escolha uma opção: ").strip()
            if op == "0":
                print("\nObrigado por usar o Citizen Assist AI Mobilidade. Até logo!")
                return
            if parece_dado_pessoal(op):
                aviso_dado_pessoal()
            elif op in acoes:
                acoes[op]()
            elif op == "":
                print("  [!] Nenhuma opção digitada. Escolha 0, 1, 2, 3 ou 4.")
            else:
                print(f"  [!] Opção \"{op}\" não existe. Escolha 0, 1, 2, 3 ou 4.")
    except Sair:
        print("\n\nEntrada encerrada. Até logo!")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
