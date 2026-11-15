

# AulaCerta 📐

Gerador de planos de aula de Matemática (6º ao 9º ano) com habilidades da BNCC **conferidas numa base oficial**.

Trabalho da disciplina Fundamentos de Inteligência Artificial, professor Marcos Assunção.
Grupo: Aliny, Bernardo, Henrique, Ranya.

## O problema

Professores gastam horas montando planos de aula alinhados à BNCC. Ferramentas de IA já ajudam, mas nos nossos testes elas citaram habilidades que existem e não combinam com o tema. O Gemini, por exemplo, usou a EF08MA07 (equação com duas incógnitas) numa aula de equação com uma incógnita. O AulaCerta resolve isso: a IA só pode escolher habilidades que o código encontrou na base, e o plano passa por uma verificação antes de chegar ao professor.

## Como funciona

```
Formulário do professor
   ↓
Prompt 1 · Análise do pedido (Step-Back + Least-to-Most) → subtópicos e palavras-chave
   ↓
Busca na base BNCC (código, sem IA) → habilidades candidatas
   ↓
Prompt 2 · Seleção de habilidades (Few-shot + Chain-of-Thought) → principal ou retomada
   ↓
Prompt 3 · Redação do plano (Role Prompt + modelo fixo em JSON)
   ↓
Prompt 4 · Verificação (Chain-of-Verification) + conferência pelo código
   ↓
Plano final + relatório de verificação → o professor revisa
```

O que é exato fica com o código, não com a IA:

- códigos BNCC fora da base são descartados;
- o tipo "retomada" é decidido pela série da habilidade;
- o texto oficial de cada habilidade vem do CSV;
- a soma dos tempos das etapas é conferida com a duração pedida.

## Minha parte

Projeto em grupo (Aliny, Bernardo, Henrique e Ranya). Eu escrevi os prompts, conduzi os 3 casos de teste (8º, 6º e 9º ano) registrados em logs e redigi este README e a apresentação.

## Como rodar

1. Instale o Python 3.10 ou mais novo.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Copie `.env.example` para `.env` e coloque a chave da API da OpenAI:
   ```
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4o-mini
   ```
   A API da OpenAI é paga à parte da assinatura do ChatGPT: é preciso colocar crédito em platform.openai.com. Cada plano faz 4 chamadas ao modelo, e com um modelo pequeno o custo por plano é de frações de centavo de dólar.
4. Abra a aplicação:
   ```bash
   streamlit run app.py
   ```
5. Para rodar os 3 casos de teste e gerar os logs:
   ```bash
   python testar_casos.py
   ```

## Arquivos

| Arquivo | O que faz |
| --- | --- |
| `app.py` | Tela em Streamlit: formulário, plano, verificação e a cadeia de prompts passo a passo |
| `cadeia.py` | Executa a cadeia, valida cada saída, confere códigos e tempos e grava o log |
| `prompts.py` | Os 4 prompts |
| `bncc.py` | Carrega a base e faz a busca por palavras-chave |
| `bncc_matematica.csv` | As 121 habilidades de Matemática do 6º ao 9º ano |
| `testar_casos.py` | Roda os 3 casos de teste |
| `logs/` | Um JSON por execução, com a saída de cada prompt (criada ao rodar) |

## Casos de teste

| Caso | Série | Tema | Duração | O que testa |
| --- | --- | --- | --- | --- |
| 1 | 8º ano | Equações do 1º grau | 50 min | Marca EF07MA18 como retomada e descarta EF08MA07? |
| 2 | 6º ano | Adição e subtração de frações | 50 min | Pré-requisitos e adaptação a uma turma com dificuldade |
| 3 | 9º ano | Teorema de Pitágoras | 100 min | A soma dos tempos fecha numa aula dupla? |

## Limitações

- Só Matemática do 6º ao 9º ano.
- A busca é por palavras-chave. Se o tema for descrito de um jeito muito diferente da BNCC, ela pode não achar a habilidade, e nesse caso o sistema avisa em vez de inventar.
- O prompt 4 também é um modelo de linguagem e pode errar. Por isso o relatório fica visível e o professor revisa o plano antes de usar.

## Fonte dos dados

Habilidades da [Base Nacional Comum Curricular](https://basenacionalcomum.mec.gov.br/) (BRASIL, MEC, 2018), Matemática, anos finais do ensino fundamental.



 



