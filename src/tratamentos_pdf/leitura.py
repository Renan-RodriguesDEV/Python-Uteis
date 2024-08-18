# %%
import PyPDF2

# Caminho do arquivo PDF
caminho_do_pdf = r'C:\Users\renan\OneDrive\Documentos\Python Scripts\lerPDF\etica.pdf'

# Abrir o arquivo PDF em modo de leitura binária ('rb')
with open(caminho_do_pdf, 'rb') as arquivo_pdf:
    # Criar um objeto leitor de PDF
    leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)

    # Número de páginas no PDF
    num_paginas = len(leitor_pdf.pages)

    # Iterar sobre todas as páginas
    for num_pagina in range(num_paginas):
        # Obter a página atual
        pagina = leitor_pdf.pages[num_pagina]

        # Extrair o texto da página atual
        texto = pagina.extract_text()

        # Imprimir o texto
        print(f"Texto da página {num_pagina + 1}:")
        print(texto)
        print()  # Adicionar uma linha em branco entre as páginas
