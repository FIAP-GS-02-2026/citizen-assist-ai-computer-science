# Citizen Assist AI Mobilidade — Computer Science

**FIAP · Ciência da Computação 1CCR · Global Solutions 2 (2026)**

Módulo de decisão lógica do projeto **Citizen Assist AI Mobilidade**. Ele responde a uma dúvida comum de quem usa ônibus em São Paulo: **"Tenho direito a gratuidade no ônibus?"**

A regra foi modelada com 4 variáveis booleanas e 2 saídas. Depois foi simplificada por álgebra booleana e mapa de Karnaugh, montada como circuito lógico no simulador **Digital** e implementada em Python.

| Integrante | RM |
|---|---|
| Gabriel Fagundes | 569074 |
| Glauco Kelly | 572840 |
| Thiago Renatino | 569073 |

## Variáveis e saídas

| Variável | 1 | 0 |
|---|---|---|
| **A** | tem 60 anos ou mais | tem menos de 60 anos |
| **B** | tem deficiência ou doença com CID da lista do Bilhete Único Especial (Portaria Conjunta SMT/SMS nº 7/2020) | não tem |
| **C** | é estudante matriculado e a escola fica a 1 km ou mais de casa | não |
| **D** | atende ao critério do Passe Livre (Portaria SMT nº 50/2019, art. 23) | não atende |

| Saída | Significado | Expressão simplificada |
|---|---|---|
| **G** | orientar a pedir gratuidade | **G = A + B + C·D** |
| **M** | orientar a pedir meia tarifa de estudante | **M = C·G'** |

Forma canônica de partida: G = ΠM(0,1,2) = (A+B+C+D)(A+B+C+D')(A+B+C'+D).
Com a simplificação, o circuito de G passa de **6 portas para 2**.

## Estrutura do repositório

```
├── logica_gratuidade.py   # regra original, formas canônicas, expressão simplificada, versão NAND e orientações
├── main.py                # programa interativo (menu)
├── testes.py              # testes de equivalência (16 combinações) e de entradas inválidas
├── evidencias/
│   ├── resultado_testes.txt
│   └── prints_programa/   # capturas reais do main.py no terminal (seção 12 do relatório)
├── simulacao/
│   ├── circuito_original.dig          # circuito original (forma canônica PdS) com G e M
│   ├── circuito_reduzido.dig          # circuito simplificado: G = A + B + C·D e M = C·G'
│   ├── circuito_gratuidade.dig        # os dois circuitos ligados às mesmas entradas
│   └── prints/
│       ├── analise_digital/                # circuitos, tabela-verdade e mapas de Karnaugh (Análises → Analisar)
│       ├── circuito_original/              # circuito original com a saída M
│       └── comparacao_original_x_reduzido/ # parte superior: original · parte inferior: reduzido
└── docs/
    └── Relatorio_Tecnico_Computer_Science.pdf
```

## Como executar o programa

Requisito: **Python 3.10 ou superior**. Não há bibliotecas externas.

```bash
git clone https://github.com/FIAP-GS-02-2026/citizen-assist-ai-computer-science.git
cd citizen-assist-ai-computer-science

python main.py     # programa interativo
python testes.py   # valida as 16 combinações e as entradas inválidas (deve terminar com OK)
```

Menu do programa:

| Opção | O que faz |
|---|---|
| 1 | Consulta guiada: responda `s` ou `n` às quatro perguntas |
| 2 | Consulta por bits: digite as entradas ABCD, por exemplo `0010` |
| 3 | Mostra a tabela-verdade completa |
| 4 | Sobre: variáveis, fontes e limitações |
| 0 | Sair |

Entradas inválidas (opção inexistente, texto vazio, bits com tamanho errado) são recusadas com uma mensagem, e a pergunta é repetida. O programa **não coleta dados pessoais**: entradas com "@" ou com 8 ou mais dígitos (CPF, telefone, e-mail) são bloqueadas, e nada é gravado.

## Como abrir a simulação no Digital

1. Instale o Java e baixe o **Digital**: https://github.com/hneemann/Digital
2. Abra um dos arquivos da pasta `simulacao/` (menu Arquivo → Abrir): `circuito_original.dig`, `circuito_reduzido.dig` ou `circuito_gratuidade.dig`.
3. Clique em **Iniciar simulação** (botão Play) e alterne as chaves A, B, C e D com o mouse.
4. Para ver a tabela-verdade e o mapa de Karnaugh gerados a partir do circuito, use **Análises → Analisar** e, na janela da tabela, a opção **K-Map**.

Em `circuito_gratuidade.dig`, a **parte superior** do arquivo é o **circuito original** (6 portas para G e 2 para M). A **parte inferior** é o **circuito reduzido** (2 portas para G e 2 para M). Os dois estão ligados às mesmas chaves, e as lâmpadas G e M de cima e de baixo devem ser iguais em todas as combinações. Na simulação, o fio verde-claro vale 1 e o verde-escuro vale 0.

## Aviso

Este protótipo **não é canal oficial** e **não confirma** a concessão de benefícios. As regras foram simplificadas para fins didáticos e conferidas em 17/11/2026. Confirme sempre na SPTrans (https://www.sptrans.com.br) ou na Central 156 da Prefeitura de São Paulo.
