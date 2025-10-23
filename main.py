from pathlib import Path
import cv2
import argparse
import numpy as np

# função para codificar o watermarking em uma imagem
def cod_watermarking(img_entrada_path: Path, fator: int, img_watermarking_path: Path):
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

    c_water, l_water = 0, 0 
    for canal in range(3):
        for l in range(linha_original):
            for c in range(coluna_original):
                if c_water >= coluna_water:
                    c_water = 0
                    l_water += 1

                pixel_w = img_watermarking[c_water, l_water, canal]
                pixel_o = img_original[l, c, canal]

                pixel_alt = int(pixel_o) + (int(pixel_w) * fator)

                while pixel_alt >= 255:
                    pixel_alt = pixel_alt - 255

                img_original[l, c, canal] = pixel_alt
                
                c_wate += 1

    

