from pathlib import Path
import cv2
import argparse
import numpy as np

# função para codificar o watermarking em uma imagem
def cod_watermarking(img_entrada_path: Path, img_watermarking_path: Path, img_out: Path, fator: int):
    # salva imagem original em uma váriavel
    img_original = cv2.imread(str(img_entrada_path), cv2.IMREAD_COLOR)
    if img_original is None:
        raise FileNotFoundError("Arquivo da imagem de entrada não encontrado!")
    
    # salva imagem do watermarking em uma váriavel
    img_watermarking = cv2.imread(str(img_watermarking_path), cv2.IMREAD_COLOR)
    if img_watermarking is None:
        raise FileNotFoundError("Arquivo do watermarking não encontrado!")

    linha_original, coluna_original, _ = img_original.shape
    linha_water, coluna_water, _ = img_watermarking.shape

    # verificar se a imagem é maior ou igual ao watermarking
    tamanho_original = linha_original * coluna_original
    tamanho_watermarking = linha_water * coluna_water
    if tamanho_watermarking > tamanho_original:
        raise ValueError("Imagem de entrada é menor que o watermarking!")

    img_alt = img_original.copy()
    # adição do watermarking na imagem
    c_water, l_water = 0, 0 
    for canal in range(3):
        for l in range(linha_original):
            for c in range(coluna_original):
                if c_water >= coluna_water:
                    c_water = 0
                    l_water += 1
                # retorna valor do pixel do watermarking e da imagem original
                pixel_w = img_watermarking[c_water, l_water, canal]
                pixel_o = img_alt[l, c, canal]

                # aplica o fator do watermarking
                pixel_alt = int(pixel_o) + (int(pixel_w) * fator)

                # trata pixel com valor maior ou igual a 255
                while pixel_alt >= 255:
                    pixel_alt = pixel_alt - 255

                # atualiza valor do pixel na imagem original
                img_alt[l, c, canal] = pixel_alt
                
                c_wate += 1

    cv2.imwrite(str(img_out), img_alt)
    
# função para decodificar o watermarking de uma imagem 
def decod_watermarking(img_entrada_path: Path, img_out: Path, fator: int):
    img_water = cv2.imread(str(img_entrada_path), cv2.IMREAD_COLOR)

# argumentos recebidos para execução do código
PARSER = argparse.ArgumentParser(prog='Watermarking Codificator and Decodificator')
PARSER.add_argument('-i', '--input-img', required=True, help='Caminho da imagem onde o watermarking vai ser adicionado ou retirado')
PARSER.add_argument('-w', '--watermarking-img', required=False, help='Caminho da imagem do watermarking que será adicionado a imagem')
PARSER.add_argument('-o', '--output-img', required=True, help='Caminho da saída da imagem com watermarking ou do próprio watermarking')
PARSER.add_argument('-f', '--factor', required=True, help='Fator de escala usado na criação e na extração do watermarking')
PARSER.add_argument('--add', action='store_true', help='Flag usada para adicionar o watermarking em uma imagem')
PARSER.add_argument('--extract', action='store_true', help='Flag usada para extraír o watermarking de uma imagem')

if __name__ == '__main__':
    args = PARSER.parse_args()

    input_path = Path(args.input_img)
    output_path = Path(args.output_img)
    fator = int(args.factor)

    if args.add:
        if not args.watermarking_img:
            PARSER.error('-w/--watermarking-img é obrigatório para --add')
        cod_watermarking(input_path, args.watermarking_img, output_path, fator)
    elif args.extract:
        decod_watermarking(input_path, output_path, fator)
    else:
        PARSER.error('Necessário usar flag --add ou --extract')