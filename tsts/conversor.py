import pandas as pd

xls = pd.ExcelFile("tsts/Ramais_testes.xlsx")
dados = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

print(dados.columns)

def converter_lis_pesquisa():
    grouped_data = {}
    html_output = "<head><link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\"><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"></head><div class=\"mt-5 ms-n1\"><p style=\"text-align: center; column-span: 2;\"><strong>        LISTA COMPLETA DE RAMAIS</strong></p><p style=\"text-align: center; column-span: 2\">        Para pesquisar, expanda a lista e pressione 'Ctrl' + 'F'</p><a class=\"toggle closed\">EXIBIR TODOS OS RAMAIS</a><div class=\"conteudo\"><div class=\"d-flex justify-content-center\"><table><tbody>"

    for index, row in dados.iterrows():

        valor_ramal = str(row["ramal"])

        
        if len(valor_ramal) > 4 :
            valor_ramal = valor_ramal[:-2]
        else:
            valor_ramal = valor_ramal

        if len(valor_ramal) < 4 :
            valor_ramal = f'0{valor_ramal}'
        else:
            valor_ramal = valor_ramal

        ramal_f = f"<tr><td><p>{row['nome']}</p></td><td><p class=\"text-nowrap\" style=\"text-align: end;\"><span>{valor_ramal}</span></p></td></tr>"
        gdsu_unidade = row['Unidade']

        if gdsu_unidade not in grouped_data:
            grouped_data[gdsu_unidade] = []

        # Adiciona o ramal no subgrupo
        grouped_data[gdsu_unidade].append(ramal_f)

    # Começa a criação do HTML com a lista de grupos
    
    for gdsu_unidade, ramais in grouped_data.items():
        html_output += f"<tr><td colspan=\"2\"><p class=\"text-center\"><strong>SETOR DE GESTÃO DA PESQUISA E DA INOVAÇÃO TECNOLÓGICA</strong></p></td></tr>"

        for ramal in ramais:
            html_output += ramal  # Adiciona os ramais na lista do grupo

    html_output += "</tbody></table></div></div></div>"  # fecha a tag das unidades
    with open('teste_html.html', 'w', encoding='utf-8') as f:
        f.write(html_output)

converter_lis_pesquisa()