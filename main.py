from pathlib import Path
import cv2
import argparse
import numpy as np

# função para codificar o watermarking em uma imagem
def cod_watermarking(img_entrada_path: Path, img_watermarking_path: Path, img_out: Path, fator: float):
    # salva imagem original em uma váriavel
    img_original = cv2.imread(str(img_entrada_path), cv2.IMREAD_COLOR)
    if img_original is None:
        raise FileNotFoundError(f"Arquivo da imagem de entrada ({img_entrada_path}) não encontrado!")
    
    # salva imagem do watermarking em uma váriavel
    img_watermarking = cv2.imread(str(img_watermarking_path), cv2.IMREAD_COLOR)
    if img_watermarking is None:
        raise FileNotFoundError(f"Arquivo do watermarking ({img_watermarking_path}) não encontrado!")

    linha_original, coluna_original, _ = img_original.shape
    linha_water, coluna_water, _ = img_watermarking.shape

    # verificar se a imagem é maior ou igual ao watermarking
    tamanho_original = linha_original * coluna_original
    tamanho_watermarking = linha_water * coluna_water
    if tamanho_watermarking != tamanho_original:
        # caso o tamanho da imagem e do watermarking seja diferente, adapta o tamanho do watermarking
        img_watermarking = cv2.resize(img_watermarking, (coluna_original, linha_original))
        linha_water, coluna_water, _ = img_watermarking.shape

    img_alt = img_original.copy()
    # adição do watermarking na imagem
    for l in range(linha_water):
            for c in range(coluna_water):
                # insere o watermarking nos 3 canais da imagem    
                for canal in range(3):
                    # retorna valor do pixel do watermarking e da imagem original
                    pixel_w = img_watermarking[l, c, canal]
                    pixel_o = img_alt[l, c, canal]

                    # transforma os pixels extraidos em float
                    pixel_w = pixel_w.astype(np.float32)
                    pixel_o = pixel_o.astype(np.float32)

                    # aplica o fator do watermarking
                    pixel_alt = pixel_o + (pixel_w * fator)

                    # trata pixel com valor maior ou igual a 255
                    pixel_alt = np.clip(pixel_alt, 0, 255).astype(np.uint8)

                    # atualiza valor do pixel na imagem original
                    img_alt[l, c, canal] = pixel_alt
                
    cv2.imwrite(str(img_out), img_alt)
    print(f"Watermarking adicionado e salvo em: {img_out}")
    
# função para decodificar o watermarking de uma imagem 
def decod_watermarking(img_entrada_path: Path, img_clean_path: Path, img_out: Path, fator: float):
    # salva imagem com watermarking em uma váriavel
    img_input = cv2.imread(str(img_entrada_path), cv2.IMREAD_COLOR)
    if img_input is None:
        raise FileNotFoundError(f"Arquivo da imagem de entrada ({img_entrada_path}) não encontrado!")

    # salva imagem original (sem watermarking) em um arquivo
    img_clean = cv2.imread(str(img_clean_path), cv2.IMREAD_COLOR)
    if img_clean is None:
        raise FileNotFoundError(f"Arquivo da imagem original ({img_clean_path}) não encontrado!")

    # extraí linhas e colunas das imagens
    linha_input, coluna_input, _ = img_input.shape
    linha_clean, coluna_clean, _ = img_clean.shape
    tamanho_input = linha_input * coluna_input
    tamanho_clean = linha_clean * coluna_clean

    if tamanho_input != tamanho_clean:
        raise ValueError("A imagem original e a imagem com watermarking não tem as mesmas dimensões!")

    # cria uma imagem em branco para armazenar o watermarking
    img_water = np.zeros((linha_clean,coluna_clean,3), dtype=np.uint8)

    # extrai watermarking da imagem
    for l in range(linha_clean):
        for c in range(coluna_clean):
            for canal in range(3):
                pixel_i = img_input[l, c, canal]
                pixel_c = img_clean[l, c, canal]

                # transforma os pixels extraidos em float
                pixel_i = pixel_i.astype(np.float32)
                pixel_c = pixel_c.astype(np.float32)

                pixel_w = (pixel_i - pixel_c) / fator

                # trata pixel com valor maior que 255 ou menor que 0
                pixel_w = np.clip(pixel_w, 0, 255).astype(np.uint8)

                img_water[l, c, canal] = pixel_w

    cv2.imwrite(str(img_out), img_water)
    print(f"Watermarking extraído para: {img_out}")


# argumentos recebidos para execução do código
PARSER = argparse.ArgumentParser(prog='Watermarking Codificator and Decodificator')
PARSER.add_argument('-i', '--input-img', required=True, help='Caminho da imagem onde o watermarking vai ser adicionado ou retirado')
PARSER.add_argument('-w', '--watermarking-img', required=False, help='Caminho da imagem do watermarking que será adicionado a imagem')
PARSER.add_argument('-o', '--output-img', required=True, help='Caminho da saída da imagem com watermarking ou do próprio watermarking')
PARSER.add_argument('-f', '--factor', required=True, help='Fator de escala usado na criação e na extração do watermarking')
PARSER.add_argument('-c', '--clean-img', required=False, help='Caminho da imagem original, sem o watermarking')
PARSER.add_argument('--add', action='store_true', help='Flag usada para adicionar o watermarking em uma imagem')
PARSER.add_argument('--extract', action='store_true', help='Flag usada para extraír o watermarking de uma imagem')

if __name__ == '__main__':
    args = PARSER.parse_args()

    input_path = Path(args.input_img)
    output_path = Path(args.output_img)
    fator = float(args.factor)

    if args.add:
        if not args.watermarking_img:
            PARSER.error('-w/--watermarking-img é obrigatório para --add')
        cod_watermarking(input_path, args.watermarking_img, output_path, fator)
    elif args.extract:
        if not args.clean_img:
            PARSER.error('-c/--clean-img é obrigatório para --extract')
        decod_watermarking(input_path, args.clean_img, output_path, fator)
    else:
        PARSER.error('Necessário usar flag --add ou --extract')