import datetime

from docx import Document


def create_document(
    vendedor: str,
    rg_vendedor: str,
    cpf_vendedor: str,
    comprador: str,
    rg_comprador: str,
    cpf_comprador: str,
    vendedor_cidade: str,
    comprador_cidade: str,
    imovel_descricao: str,
    metros: float,
    endereco: str,
    valor_moeda: str,
    valor_extenso: str,
    cidade: str,
    input_file="base.docx",
    output_file="contract.docx",
):
    document = Document(input_file)
    data = datetime.datetime.now()
    dia = data.day
    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    mes = meses[data.month - 1]
    ano = data.year

    params = {
        "{{VENDEDOR}}": vendedor,
        "{{RG_VENDEDOR}}": rg_vendedor,
        "{{CPF_VENDEDOR}}": cpf_vendedor,
        "{{COMPRADOR}}": comprador,
        "{{RG_COMPRADOR}}": rg_comprador,
        "{{CPF_COMPRADOR}}": cpf_comprador,
        "{{C_VENDEDOR}}": vendedor_cidade,
        "{{C_COMPRADOR}}": comprador_cidade,
        "{{IMOVEL}}": imovel_descricao,
        "{{METROS}}": metros,
        "{{ENDERECO}}": endereco,
        "{{VALOR_MOEDA}}": valor_moeda,
        "{{VALOR_EXTENSO}}": valor_extenso,
        "{{CIDADE}}": cidade,
        "{{DD}}": dia,
        "{{MM}}": mes,
        "{{AAAA}}": ano,
    }
    for p in document.paragraphs:
        for param in params:
            p.text = p.text.replace(param, str(params[param]))
            print(f"Substituindo [{param}] por [{params[param]}]")
    document.save(f"documents/{output_file}")
    print(
        f"Document save sucessfully!! please check outputfile in : documents/{output_file}"
    )
    return output_file
