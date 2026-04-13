# Image Watermarking & Extraction Tool

Uma ferramenta de linha de comando (CLI) desenvolvida em Python para codificação e decodificação de marcas d'água invisíveis ou visíveis em imagens digitais, utilizando manipulação direta de matrizes de pixels via OpenCV.

## Sobre o Projeto

Este repositório tem como objetivo fornecer um utilitário prático e de alta performance para inserir e extrair informações visuais em mídias. O algoritmo atua no **domínio espacial** da imagem, iterando sobre os canais RGB e modificando os valores originais com base em um fator de escala multiplicativo.

Do ponto de vista de **Segurança da Informação e Forense Digital**, esta ferramenta serve como uma excelente base de estudo e aplicação para:
* **Esteganografia (Data Hiding):** Ocultação de assinaturas ou dados dentro de uma imagem portadora.
* **Rastreabilidade:** Inserção de identificadores para rastrear a origem de vazamentos de dados.
* **Autenticidade:** Comprovação de que uma mídia não foi adulterada (através da extração reversa comparada com a imagem limpa).

## Como Funciona

* **Codificação (`--add`):** O script lê a imagem de entrada e a imagem da marca d'água. Ele mapeia os pixels da marca d'água sobre a imagem original, somando os valores dos canais RGB multiplicados por um `fator` de intensidade, garantindo que o valor final respeite o limite de 8-bits (módulo 255).
* **Decodificação (`--extract`):** Requer a imagem previamente marcada e a imagem original (limpa). O script subtrai a imagem limpa da imagem marcada e divide pelo `fator` utilizado na criação, reconstruindo a marca d'água original e salvando-a como um novo artefato.

## Tecnologias e Pré-requisitos

Para rodar este script, você precisará do Python instalado e de bibliotecas de manipulação matricial e de visão computacional.

**Dependências Python:**
```bash
pip install opencv-python numpy
