import cv2

import tkinter as tk 
from tkinter import filedialog

root = tk.Tk() 
root.withdraw()

file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")]) 

if file_path: 
  imagem = cv2.imread(file_path)
  imagem_2 = cv2.resize(imagem, (500,500))
  question = input("Transformar em preto e branco? (s/n): ")
  if question == 's':
    for y in range(0, imagem_2.shape[0]):
      for x in range(0, imagem_2.shape[1]):
        (azul,verde,vermelho) = imagem_2[y,x]
        imagem_2[y,x] = (azul*0.114+verde*0.587+vermelho*0.299)
    cv2.imshow('Teste',imagem_2)
    cv2.waitKey(0)
  elif question == 'n':
    for y in range(0, imagem_2.shape[0]):
      for x in range(0, imagem_2.shape[1]):
        (azul,verde,vermelho) = imagem_2[y,x]
        imagem_2[y,x] = (azul,verde,vermelho)
    cv2.imshow('Teste',imagem_2)
    cv2.waitKey(0)
  else:
    print('Entrada inválida') 
else: 
    print("Arquivo não selecionado") 