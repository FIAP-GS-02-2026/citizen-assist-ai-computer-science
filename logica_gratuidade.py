"""
Citizen Assist AI Mobilidade - Módulo de decisão lógica (Computer Science)

Situação de atendimento: "Tenho direito a andar de graça no ônibus municipal?"
(regras simplificadas do transporte municipal de São Paulo - SPTrans)

Variáveis de entrada (1 = sim, 0 = não):
    A - a pessoa tem 60 anos ou mais (Decreto nº 58.639/2019, art. 36, na redação
        do Decreto nº 62.057/2022; cadastro exige residência na Região Metropolitana
        ou em município de portaria da SMT - art. 37)
    B - a pessoa tem deficiência ou doença cujo CID consta do Anexo Único da
        Portaria Conjunta SMT/SMS nº 7/2020 (Decreto nº 58.639/2019, art. 38):
        deficiências físicas, intelectuais, mentais, visuais e auditivas e também
        doenças como HIV, câncer em tratamento e insuficiência renal em diálise,
        cada uma com requisitos próprios, comprovados por Formulário de Solicitação
        médico e avaliados pela SPTrans
    C - a pessoa é estudante matriculado em curso reconhecido e a escola fica a
        1 km ou mais de casa, com ligação por transporte coletivo (Decreto nº
        58.639/2019, art. 29, § 1º - vale para meia tarifa e para gratuidade)
    D - a pessoa atende ao critério do Bilhete Único de Estudante com Gratuidade
        (Passe Livre), Portaria SMT nº 50/2019, art. 23, que regulamenta o Decreto
        nº 58.639/2019; base legal: Lei nº 8.424/1976, art. 12, § 1º, na redação
        do art. 15 da Lei nº 16.097/2014:
          I   fundamental, médio, técnico, tecnólogo ou profissionalizante na rede pública;
          II  superior público com renda familiar per capita < 1,5 salário mínimo;
          III superior privado com renda < 1,5 SM, OU bolsista ProUni, financiado
              pelo FIES, integrante do Bolsa Universidade (Escola da Família) ou
              de cotas sociais;
          IV  técnico, tecnológico ou profissionalizante privado com renda < 1,5 SM.

Saídas:
    G - 1 = orientar a pedir GRATUIDADE (tarifa zero); 0 = não há gratuidade pelas regras modeladas
    M - 1 = orientar a pedir MEIA TARIFA de estudante; 0 = não se aplica

Este arquivo contém as várias representações da MESMA função lógica, usadas
para provar a equivalência nos testes:
    regra_original      -> regras em linguagem natural (if/else)
    g_soma_mintermos    -> forma canônica SdP: soma dos 13 mintermos
    g_produto_maxtermos -> forma canônica PdS: produto dos 3 maxtermos
    g_simplificada      -> A + B + C·D (álgebra booleana e Karnaugh)
    g_nand              -> forma obtida com De Morgan: ( A'·B'·(C·D)' )'
"""

from dataclasses import dataclass

DATA_CONSULTA = "17/11/2026"

VARIAVEIS = {
    "A": ("Tem 60 anos ou mais?",
          "1 = tem 60 anos ou mais | 0 = tem menos de 60 anos"),
    "B": ("Tem deficiência ou doença com CID da lista do Bilhete Único Especial (física, intelectual, "
          "mental, visual, auditiva ou doenças como HIV, câncer em tratamento e insuficiência renal em "
          "diálise) e um médico pode preencher o Formulário de Solicitação?",
          "1 = tem condição da lista, com relatório médico | 0 = não tem"),
    "C": ("É estudante matriculado e a escola fica a 1 km ou mais da sua casa?",
          "1 = é estudante e mora a 1 km ou mais da escola | 0 = não"),
    "D": ("Estuda na rede pública (fundamental, médio, técnico, tecnólogo ou profissionalizante); OU faz "
          "superior público com renda familiar por pessoa abaixo de 1,5 salário mínimo; OU faz superior "
          "privado com ProUni, FIES, Bolsa Universidade (Escola da Família), cotas sociais ou renda por "
          "pessoa abaixo de 1,5 salário mínimo; OU faz técnico/profissionalizante privado com renda por "
          "pessoa abaixo de 1,5 salário mínimo?",
          "1 = atende ao critério do Passe Livre | 0 = não atende"),
}

FONTES = [
    ("Estatuto da Pessoa Idosa - Lei Federal nº 10.741/2003, art. 39 (gratuidade a partir de 65 anos)",
     "https://www.planalto.gov.br/ccivil_03/leis/2003/l10.741.htm"),
    ("Decreto Municipal nº 62.057/2022 - restabelece a gratuidade a partir de 60 anos (altera os arts. 36 e 37 "
     "do Decreto nº 58.639/2019)",
     "https://legislacao.prefeitura.sp.gov.br/decreto-62057-de-14-de-dezembro-de-2022"),
    ("Prefeitura de São Paulo - SPTrans envia novo cartão do Bilhete Único para passageiros entre 60 e 64 anos",
     "https://prefeitura.sp.gov.br/w/noticia/sptrans-vai-enviar-novo-cartao-do-bilhete-unico-para-passageiros-entre-60-e-64-anos"),
    ("Prefeitura de São Paulo - SPTrans oferece serviços de acessibilidade para pessoas com deficiência "
     "(Bilhete Único Especial)",
     "https://prefeitura.sp.gov.br/w/noticia/sptrans-oferece-servicos-de-acessibilidade-para-pessoas-com-deficiencia"),
    ("Câmara Municipal de São Paulo - Executivo define regras do passe livre para estudantes",
     "https://www.saopaulo.sp.leg.br/blog/passe-livre/"),
    ("SPTrans - Canal do Estudante (Bilhete Único Estudante: Passe Livre e meia tarifa)",
     "http://estudante.sptrans.com.br"),
    ("SPTrans - site oficial (Bilhete Único e atendimento)", "https://www.sptrans.com.br"),
    ("Decreto Municipal nº 58.639/2019 - regulamento consolidado do Bilhete Único (gratuidades e cadastro)",
     "https://legislacao.prefeitura.sp.gov.br/decreto-58639-de-22-de-fevereiro-de-2019"),
    ("Decreto Municipal nº 64.127/2025 - institui o Programa Mamãe Tarifa Zero",
     "https://legislacao.prefeitura.sp.gov.br/decreto-64127-de-28-de-marco-de-2025"),
    ("Portaria Conjunta SMT/SMS nº 7/2020 - Anexo Único: relação de CIDs, requisitos, acompanhante e "
     "validade do Bilhete Único Especial da Pessoa com Deficiência",
     "https://legislacao.prefeitura.sp.gov.br/portaria-conjunta-secretaria-municipal-de-mobilidade-e-transportes-smt-secretaria-municipal-da-saude-sms-7-de-26-de-agosto-de-2020/anexo/5f512f2014119228d21604b7/Anexo%20%C3%9Anico%20da%20Portaria%20Conjunta%20SMT-SMS%20n%C2%BA%207_2020.pdf"),
    ("Lei Municipal nº 16.097/2014, art. 15 - dá nova redação ao art. 12, § 1º, da Lei nº 8.424/1976 e "
     "autoriza a isenção integral da tarifa a estudantes",
     "https://legislacao.prefeitura.sp.gov.br/leis/lei-16097-de-29-de-dezembro-de-2014"),
    ("Portaria SMT nº 50/2019 - disciplina o Bilhete Único (Decreto nº 58.639/2019); arts. 22 e 23: "
     "estudante meia tarifa e estudante com gratuidade",
     "https://legislacao.prefeitura.sp.gov.br/leis/portaria-secretaria-municipal-de-mobilidade-e-transportes-"
     "smt-50-de-5-de-abril-de-2019"),
]

AVISO = ("Este assistente NÃO é canal oficial e NÃO confirma a concessão de benefícios. "
         f"Regras simplificadas, conferidas em {DATA_CONSULTA}. Confirme sempre na SPTrans "
         "(sptrans.com.br) ou na Central 156 da Prefeitura de São Paulo.")

LIMITACOES = [
    "Modela apenas os ônibus municipais da cidade de São Paulo (SPTrans); metrô, trem e EMTU têm regras próprias.",
    "Usa 4 perguntas de sim/não; casos especiais (acompanhante de pessoa com deficiência, Bilhete Único "
    "da Gestante, conselheiros participativos, decisões judiciais) não estão modelados.",
    "O Programa Mamãe Tarifa Zero (Decreto nº 64.127/2025: acompanhante maior de 18 anos, inscrito no "
    "CadÚnico, de criança matriculada em CEI da rede municipal, morando a mais de 1,5 km, só no trajeto "
    "casa-escola, sem outro transporte gratuito e sem Bilhete Único Especial ativo) não entra nas "
    "variáveis A-D; aparece apenas como orientação complementar.",
    "Residência (Região Metropolitana ou município de portaria da SMT) e distância até a escola "
    "(1 km ou mais, com ligação por transporte coletivo) estão resumidas nas perguntas A e C, sem verificação.",
    "Os critérios do Passe Livre seguem a Portaria SMT nº 50/2019, art. 23. O programa usa a regra "
    "'abaixo de 1,5 salário mínimo per capita' e não cita valores em reais, que mudam todo ano.",
    "Um estudante que já tem outro benefício tarifário (idoso ou pessoa com deficiência) não acumula a "
    "gratuidade de estudante (Portaria SMT nº 50/2019, art. 23, § 2º); no modelo isso não muda a saída, "
    "porque G já vale 1.",
    "Não verifica documentos: a concessão depende de cadastro e análise da SPTrans.",
    "A pergunta B resume a lista de cerca de 140 CIDs da Portaria Conjunta SMT/SMS nº 7/2020; o programa "
    "não confere o CID nem os requisitos de cada um (grau de limitação, tratamento em curso, idade), nem "
    "decide sobre acompanhante e validade. Também não trata metrô e CPTM, que têm exigências extras.",
    "O limite de renda (abaixo de 1,5 salário mínimo per capita) e os documentos exigidos podem mudar; confira a "
    "data de consulta das fontes.",
    "Não coleta nome, CPF, idade exata, endereço ou qualquer dado pessoal. Nada é gravado.",
]


# ---------------------------------------------------------------------------
# 1) Regra original, escrita como o atendente explicaria em linguagem natural
# ---------------------------------------------------------------------------
def regra_original(a: int, b: int, c: int, d: int) -> int:
    """G: a pessoa tem direito a pedir gratuidade?"""
    if a == 1:          # 60+ (Decreto 58.639/2019, art. 36, redação do Decreto 62.057/2022)
        return 1
    if b == 1:          # CID da Portaria Conjunta SMT/SMS 7/2020 -> Bilhete Único Especial
        return 1
    if c == 1:          # estudante a 1 km ou mais da escola (art. 29, § 1º)...
        if d == 1:      # ...que se enquadra na Portaria 003/15-SMT.GAB tem Passe Livre
            return 1
        return 0        # ...que não atende paga meia (não é gratuidade)
    return 0            # demais casos pagam a tarifa


def regra_original_meia(a: int, b: int, c: int, d: int) -> int:
    """M: estudante que não tem gratuidade por nenhum motivo paga meia tarifa."""
    if regra_original(a, b, c, d) == 1:
        return 0        # quem já tem gratuidade não precisa de meia
    return 1 if c == 1 else 0


# ---------------------------------------------------------------------------
# 2) Formas canônicas (montadas a partir da tabela-verdade)
#    índice do mintermo = 8A + 4B + 2C + D
# ---------------------------------------------------------------------------
MINTERMOS_G = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
MAXTERMOS_G = (0, 1, 2)
MINTERMOS_M = (2,)


def _n(x: int) -> int:
    return 1 - x


def g_soma_mintermos(A, B, C, D):
    """G = Σm(3,4,5,6,7,8,9,10,11,12,13,14,15)."""
    An, Bn, Cn, Dn = _n(A), _n(B), _n(C), _n(D)
    termos = [
        An & Bn & C & D,     # m3  0011
        An & B & Cn & Dn,    # m4  0100
        An & B & Cn & D,     # m5  0101
        An & B & C & Dn,     # m6  0110
        An & B & C & D,      # m7  0111
        A & Bn & Cn & Dn,    # m8  1000
        A & Bn & Cn & D,     # m9  1001
        A & Bn & C & Dn,     # m10 1010
        A & Bn & C & D,      # m11 1011
        A & B & Cn & Dn,     # m12 1100
        A & B & Cn & D,      # m13 1101
        A & B & C & Dn,      # m14 1110
        A & B & C & D,       # m15 1111
    ]
    r = 0
    for t in termos:
        r |= t
    return r


def g_produto_maxtermos(A, B, C, D):
    """G = ΠM(0,1,2) = (A+B+C+D)·(A+B+C+D')·(A+B+C'+D)."""
    M0 = A | B | C | D
    M1 = A | B | C | _n(D)
    M2 = A | B | _n(C) | D
    return M0 & M1 & M2


# ---------------------------------------------------------------------------
# 3) Expressão simplificada (álgebra booleana = mapa de Karnaugh)
# ---------------------------------------------------------------------------
def g_simplificada(A, B, C, D):
    """G = A + B + C·D."""
    return A | B | (C & D)


def g_nand(A, B, C, D):
    """De Morgan: G = (A' · B' · (C·D)')'  -> implementável só com NOT/NAND."""
    nand_cd = _n(C & D)
    return _n(_n(A) & _n(B) & nand_cd)


def m_canonica(A, B, C, D):
    """M = m2 = A'·B'·C·D'."""
    return _n(A) & _n(B) & C & _n(D)


def m_simplificada(A, B, C, D):
    """M = C · G'  (reaproveita a saída G já calculada)."""
    return C & _n(g_simplificada(A, B, C, D))


# ---------------------------------------------------------------------------
# Orientações em linguagem simples
# ---------------------------------------------------------------------------
@dataclass
class Orientacao:
    g: int
    m: int
    titulo: str
    passos: list
    fontes: list


def orientar(A: int, B: int, C: int, D: int) -> Orientacao:
    """Usa a LÓGICA SIMPLIFICADA (G = A + B + CD, M = C·G') para escolher a orientação."""
    for v in (A, B, C, D):
        if v not in (0, 1):
            raise ValueError("As entradas devem ser 0 ou 1.")
    g = g_simplificada(A, B, C, D)
    m = m_simplificada(A, B, C, D)
    passos, fontes = [], []
    if g:
        titulo = "Você pode ter direito à GRATUIDADE (tarifa zero) no ônibus municipal."
        if A:
            passos.append(
                "Pessoa com 60 anos ou mais (Decreto nº 58.639/2019, art. 36): embarque pela porta dianteira e "
                "use o Bilhete Único Especial da Pessoa Idosa, ou mostre documento oficial com foto (RG) e "
                "desembarque pela mesma porta. O cartão é obtido com cadastro na SPTrans, comprovando residência "
                "na Região Metropolitana ou em município conveniado, como Jundiaí, Campo Limpo Paulista ou "
                "Várzea Paulista (art. 37).")
            passos.append(
                "Entre 60 e 64 anos (faixa restabelecida pelo Decreto nº 62.057/2022), a SPTrans informa que a "
                "gratuidade pode ficar no Bilhete Único comum e precisa ser recarregada todo mês nos validadores "
                "do ônibus, dos terminais ou das estações.")
            fontes += [FONTES[0], FONTES[1], FONTES[2], FONTES[7]]
        if B:
            passos.append(
                "Pessoa com deficiência ou doença da lista: confira seu CID no Anexo Único da Portaria Conjunta "
                "SMT/SMS nº 7/2020. Cada CID tem requisitos próprios (ex.: grau da limitação, tratamento em curso, "
                "exames). Peça ao médico o Formulário de Solicitação e solicite o Bilhete Único Especial pelo "
                "site SPTrans Atendimento ou em um posto presencial (Descomplica SP / Subprefeituras). Conforme o "
                "CID, o benefício pode incluir acompanhante e tem validade definida (de 3 meses a 4 anos), "
                "devendo ser renovado.")
            fontes += [FONTES[9], FONTES[3]]
        if C and D:
            passos.append(
                "Estudante com Passe Livre (Bilhete Único de Estudante com Gratuidade, Portaria SMT nº 50/2019, "
                "art. 23): faça o cadastro no Portal do Bilhete Único (bilheteunico.sptrans.com.br). A "
                "instituição de ensino envia a matrícula à SPTrans. Quem se enquadra pela renda (abaixo de 1,5 "
                "salário mínimo por pessoa) preenche também a Declaração de Renda. As cotas gratuitas são "
                "mensais e valem no trajeto casa-escola.")
            fontes += [FONTES[10], FONTES[11], FONTES[5]]
    elif m:
        titulo = "Você não tem gratuidade, mas pode pagar MEIA TARIFA como estudante."
        passos.append(
            "Peça o Bilhete Único Estudante pelo Canal do Estudante da SPTrans. Com ele você paga metade da "
            "tarifa (vale no trajeto casa-escola). Se você faz superior ou curso técnico/profissionalizante e a "
            "renda familiar por pessoa ficar abaixo de 1,5 salário mínimo, ou se passar a ter ProUni, FIES, "
            "Bolsa Universidade ou cotas sociais, atualize a Declaração de Renda no Portal do Bilhete Único: "
            "você pode passar ao Passe Livre. Ensino fundamental e médio na rede privada não dão gratuidade.")
        fontes += [FONTES[11], FONTES[7], FONTES[5]]
    else:
        titulo = "Pelas regras modeladas, não há gratuidade nem meia tarifa: a tarifa é integral."
        passos.append(
            "Use o Bilhete Único comum para ter a integração entre ônibus. Se você acha que está em um caso "
            "especial não previsto aqui, consulte a SPTrans ou a Central 156. Se você leva uma criança matriculada em CEI "
            "da rede municipal e está no CadÚnico, veja o Programa Mamãe Tarifa Zero.")
        fontes += [FONTES[6], FONTES[8]]
    return Orientacao(g, m, titulo, passos, fontes)
