# Automação de Processamento de Invoices

Este projeto foi desenvolvido como parte de um desafio técnico para uma vaga de estágio em automação.  
O objetivo é extrair informações de invoices (faturas) em PDF, armazenar os dados em formato JSON e disponibilizá-los para análises simples no terminal.  

Os arquivos PDF foram obtidos do dataset público Company Documents Dataset, disponível no Kaggle:

https://www.kaggle.com/datasets/ayoubcherguelaine/company-documents-dataset

A automação é dividida em duas etapas principais:

- Extração dos dados dos PDFs
- Análise dos dados extraídos
---
## Estrutura do projeto

```

teste-tecnico-qca/
│
├── invoices-pdf/          # Pasta onde ficam os arquivos PDF
│   └── .gitkeep
│
├── models.py              # Modelos de dados usando Pydantic
├── invoice_extractor.py   # Classe responsável pela extração dos dados
├── invoice_analizer.py    # Classe responsável pela análise dos dados
│
├── run_extractor.py       # Script para executar a extração
├── run_analizer.py        # Script para executar a análise
│
└── database.json          # Arquivo JSON gerado após a extração

````

---

## Como rodar o projeto

### Pré-requisitos

- Python 3.13
- Pip

### Instalação das bibliotecas

Foram utilizadas as seguintes bibliotecas: pdfplumber, pandas e pydantic.

Para a instalação basta rodar:

```bash
pip install pdfplumber
````

```bash
pip install pandas
```

```bash
pip install pydantic
```

Ou, de forma simples:

```bash
pip install pdfplumber pandas pydantic
```

---

## Extração dos dados

1. Coloque os arquivos PDF na pasta `invoices-pdf`
2. No terminal, estando na pasta raiz do projeto, execute:

```bash
python run_extractor.py
```

O script vai:

* Ler todos os PDFs da pasta
* Extrair `orderId`, `customerId`, `date` e os produtos
* Vai evitar duplicidade de invoices usando o `orderId`
* Gerar o arquivo `database.json`

---

## Análise dos dados

Após a extração, execute:

```bash
python run_analizer.py
```

Esse script vai:

* Ler o arquivo `database.json`
* Normalizar os dados em um DataFrame
* Realizar análises
* Exibir um relatório no terminal

---

## Funcionamento das classes

### InvoiceExtractor

Classe responsável por todo o processo de extração dos dados dos PDFs.

Métodos:

* existing_ids():
  Lê o arquivo `database.json` (se existir) e retorna os `orderId` já incluidos, para no futuro conseguirmos evitar duplicidade.

* extracting_information():
  Extrai as informações dos PDFs utilizando expressões regulares (regex) e leitura de tabelas.

* save_json():
  Salva os dados extraídos no arquivo `database.json`.

---

### InvoiceAnalyzer

Classe responsável pela análise dos dados extraídos.

Principais métodos:

* normalize_invoices():
  Lê o JSON, organiza os dados e cria a coluna `total_item`, que representa o valor total gasto em cada produto que será utilizado por outras funções.

* average_invoices():
  Calcula a média do valor total das invoices.

* most_frequent_product():
  Identifica o produto que foi mais frequentemente comprado.

* total_spent_per_product():
  Calcula o total gasto por produto.

* products_price_list():
  Retorna a lista de produtos com seus preços unitários.

* print_report():
  Mostra o relatório final no terminal.

---

## Models

O arquivo `models.py` utiliza Pydantic para garantir a integridade dos dados.

* Product

  * name
  * quantity
  * unitPrice

* Invoice

  * orderId
  * customerId
  * date
  * lista de produtos

---

## Bibliotecas utilizadas

* pdfplumber – leitura e extração de dados dos PDFs
* pandas – manipulação e análise dos dados
* pydantic – validação e integridade dos dados
* re – uso de expressões regulares
* json – criação e leitura do arquivo JSON
* os – manipulação de arquivos e diretórios
* datetime – tratamento de datas