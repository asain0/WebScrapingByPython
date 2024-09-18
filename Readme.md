# Projeto de Web Scraping - Estudo de extração de dados

## Descrição
Este projeto foi realizado como estudo de web scraping, para extrair dados estruturados. O objetivo é coletar informações relevantes de páginas da web de maneira automatizada, organizar esses dados e exportá-los para um arquivo no formato desejado para análise posterior.
No arquivo `WebScrapping.py`, foi feito o exemplo de extração dos rankings de atletas da IBJJF, com base na aula do Paulo Sawaya. Já no `exercicioWebScraping.py` utilizei o primeiro arquivo como base para extrair uma lista de notícias de um site, utilizando um ou mais termos de pesquisa, dentro de um período fixo.

## Tecnologias Utilizadas
- **Requests**: Biblioteca para fazer requisições HTTP e obter o conteúdo das páginas. É usada para acessar as páginas de interesse e obter o HTML bruto.
- **BeautifulSoup**: Usada para navegar e extrair dados do HTML obtido. Facilita a busca e manipulação de elementos como tags, classes e IDs no código HTML.
- **Pandas**: Biblioteca poderosa para manipulação e análise de dados. Os dados coletados pelo web scraper são organizados em um DataFrame e exportados para Excel.

## Funcionamento do Código
1. **Extração do HTML**: Utilizando a biblioteca `requests`, o código faz requisições HTTP para o site e obtém o conteúdo da página.
2. **Processamento do HTML**: A biblioteca `BeautifulSoup` é usada para analisar o HTML e encontrar elementos específicos, como títulos, resumos, fotos e links das notícias.
3. **Organização dos Dados**: Os dados extraídos são armazenados em uma lista de dicionários e, em seguida, convertidos em um DataFrame utilizando a biblioteca `pandas`.
4. **Exportação para Excel**: Os dados estruturados são exportados para um arquivo Excel, facilitando a análise e a manipulação posterior.

## Funcionalidades de Otimização
- **Controle de Requisições**: O código implementa uma lógica de retentativas para garantir que, em caso de falha temporária (como o código de status 429 - Too Many Requests), novas tentativas sejam feitas após um intervalo de tempo. Essa implementação foi necessária, pois a partir de um número X de requisições, o servidor negava as consultas. Então implementamos um tempo de espera para depois retomar a requisição.
- **Tratamento de Exceções**: Para evitar que erros na extração interrompam o funcionamento do código, há tratamento adequado de erros e pausas entre requisições.

## Como Executar o Projeto
Como cada página possui uma estrutura própria, e a necessidade de dados pode variar de acordo com o cliente, é necessário avaliar o site que será pesquisado e implementar as regras e validações. Sendo assim, o projeto poderá servir apenas de base para outros projetos. Até mesmo o `WebScrapping.py`, em um determinado momento pode não mais funcionar, caso o site da IBJJF seja reformulado.
1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/projeto-webscraping.git

