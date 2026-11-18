"""
Validação do módulo de decisão lógica.

1. Testa as 16 combinações de entrada e prova que são equivalentes:
   regra original (if/else) = soma de mintermos = produto de maxtermos
   = expressão simplificada = versão De Morgan (NAND) = valor do mapa de Karnaugh
   = resultado do programa (função orientar).
2. Testa o tratamento de entradas inválidas do programa interativo.

Execução:  python testes.py
Gera também evidencias/resultado_testes.txt.
"""

import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest import mock

import logica_gratuidade as lg
import main

AQUI = os.path.dirname(os.path.abspath(__file__))

# Mapa de Karnaugh de G (linhas AB, colunas CD em código Gray)
GRAY = ["00", "01", "11", "10"]
KMAP_G = {
    "00": {"00": 0, "01": 0, "11": 1, "10": 0},
    "01": {"00": 1, "01": 1, "11": 1, "10": 1},
    "11": {"00": 1, "01": 1, "11": 1, "10": 1},
    "10": {"00": 1, "01": 1, "11": 1, "10": 1},
}


def combinacoes():
    for i in range(16):
        yield i, ((i >> 3) & 1, (i >> 2) & 1, (i >> 1) & 1, i & 1)


def tabela_equivalencia():
    linhas = []
    for i, (A, B, C, D) in combinacoes():
        linhas.append({
            "m": i, "A": A, "B": B, "C": C, "D": D,
            "original": lg.regra_original(A, B, C, D),
            "sop": lg.g_soma_mintermos(A, B, C, D),
            "pos": lg.g_produto_maxtermos(A, B, C, D),
            "simpl": lg.g_simplificada(A, B, C, D),
            "nand": lg.g_nand(A, B, C, D),
            "kmap": KMAP_G[f"{A}{B}"][f"{C}{D}"],
            "programa": lg.orientar(A, B, C, D).g,
            "m_original": lg.regra_original_meia(A, B, C, D),
            "m_canon": lg.m_canonica(A, B, C, D),
            "m_simpl": lg.m_simplificada(A, B, C, D),
            "m_programa": lg.orientar(A, B, C, D).m,
        })
    return linhas


class TestEquivalencia(unittest.TestCase):
    def test_16_combinacoes_saida_G(self):
        for l in tabela_equivalencia():
            with self.subTest(m=l["m"]):
                valores = {l[k] for k in ("original", "sop", "pos", "simpl", "nand", "kmap", "programa")}
                self.assertEqual(len(valores), 1, f"Divergência na combinação m{l['m']}: {l}")

    def test_16_combinacoes_saida_M(self):
        for l in tabela_equivalencia():
            with self.subTest(m=l["m"]):
                valores = {l[k] for k in ("m_original", "m_canon", "m_simpl", "m_programa")}
                self.assertEqual(len(valores), 1, f"Divergência em M na combinação m{l['m']}: {l}")

    def test_mintermos_e_maxtermos_complementares(self):
        self.assertEqual(sorted(lg.MINTERMOS_G + lg.MAXTERMOS_G), list(range(16)))
        for i, (A, B, C, D) in combinacoes():
            self.assertEqual(lg.regra_original(A, B, C, D), 1 if i in lg.MINTERMOS_G else 0)

    def test_saidas_exclusivas(self):
        """Ninguém recebe gratuidade e meia ao mesmo tempo."""
        for _, v in combinacoes():
            self.assertFalse(lg.g_simplificada(*v) and lg.m_simplificada(*v))

    def test_entrada_fora_de_0_1(self):
        with self.assertRaises(ValueError):
            lg.orientar(2, 0, 0, 0)

    def test_toda_orientacao_tem_fonte_e_texto(self):
        for _, v in combinacoes():
            o = lg.orientar(*v)
            self.assertTrue(o.titulo and o.passos and o.fontes)


def executar_programa(entradas):
    """Roda main.main() com as entradas simuladas e devolve o texto exibido."""
    saida = io.StringIO()
    # Ao acabarem as entradas, input() levanta EOFError, como num terminal real (Ctrl+D / Ctrl+Z)
    with mock.patch("builtins.input", side_effect=list(entradas) + [EOFError()]), redirect_stdout(saida):
        main.main()
    return saida.getvalue()


class TestEntradasInvalidas(unittest.TestCase):
    def test_opcao_inexistente_e_vazia(self):
        out = executar_programa(["9", "", "abc", "0"])
        self.assertIn('Opção "9" não existe', out)
        self.assertIn("Nenhuma opção digitada", out)
        self.assertIn('Opção "abc" não existe', out)
        self.assertIn("Até logo", out)

    def test_resposta_sim_nao_invalida(self):
        out = executar_programa(["1", "talvez", "", "s", "n", "n", "n", "0"])
        self.assertIn('"talvez" não é uma resposta válida', out)
        self.assertIn("Resposta vazia", out)
        self.assertIn("GRATUIDADE", out)

    def test_bloqueio_de_dados_pessoais(self):
        out = executar_programa(["1", "123.456.789-00", "fulano@email.com", "n", "n", "s", "n", "0"])
        self.assertEqual(out.count("dado pessoal"), 2)
        self.assertIn("MEIA TARIFA", out)

    def test_bits_invalidos(self):
        out = executar_programa(["2", "12", "10a1", "11111", "0011", "0"])
        self.assertEqual(out.count("Entrada inválida"), 3)
        self.assertIn("A=0  B=0  C=1  D=1", out)

    def test_fim_de_entrada_nao_quebra(self):
        out = executar_programa([])  # simula Ctrl+D / Ctrl+Z
        self.assertIn("Entrada encerrada", out)

    def test_aviso_canal_oficial(self):
        out = executar_programa(["2", "0000", "0"])
        self.assertIn("NÃO é canal oficial", out)
        self.assertIn("tarifa é integral", out)


def relatorio_texto():
    cab = (" m | A B C D | Original | SdP | PdS | Simplif. | NAND | K-map | Programa || "
           "M orig | M canon | M simpl | M prog | OK")
    linhas = [cab, "-" * len(cab)]
    for l in tabela_equivalencia():
        okg = len({l[k] for k in ("original", "sop", "pos", "simpl", "nand", "kmap", "programa")}) == 1
        okm = len({l[k] for k in ("m_original", "m_canon", "m_simpl", "m_programa")}) == 1
        linhas.append(
            f"{l['m']:2d} | {l['A']} {l['B']} {l['C']} {l['D']} |    {l['original']}     |  {l['sop']}  |  {l['pos']}  |"
            f"    {l['simpl']}     |  {l['nand']}   |   {l['kmap']}   |    {l['programa']}     ||"
            f"   {l['m_original']}    |    {l['m_canon']}    |    {l['m_simpl']}    |   {l['m_programa']}    | "
            f"{'OK' if okg and okm else 'FALHA'}")
    return "\n".join(linhas)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    tabela = relatorio_texto()
    print("TABELA DE EQUIVALÊNCIA (16 combinações)\n")
    print(tabela)
    print()
    fluxo = io.StringIO()
    runner = unittest.TextTestRunner(stream=fluxo, verbosity=2)
    resultado = runner.run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    print(fluxo.getvalue())
    os.makedirs(os.path.join(AQUI, "evidencias"), exist_ok=True)
    with open(os.path.join(AQUI, "evidencias", "resultado_testes.txt"), "w", encoding="utf-8") as f:
        f.write("TABELA DE EQUIVALÊNCIA (16 combinações)\n\n" + tabela + "\n\n" + fluxo.getvalue())
    sys.exit(0 if resultado.wasSuccessful() else 1)
