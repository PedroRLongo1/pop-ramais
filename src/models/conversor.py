from imports import *

def copy_html(label_converter):
    # Obter o texto do QLabel
    text_to_copy = label_converter.text()

    # Acessar a área de transferência
    clipboard = QApplication.clipboard()

    # Copiar o texto para a área de transferência
    clipboard.setText(text_to_copy)

def converter_lis_pub():

    xls = pd.ExcelFile("src/Ramais.xlsx")
    db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

    invisivel = "\u200B"  # Zero-width space (caractere invisível)


        # Inicializa o dicionário para agrupar os dados
    grouped_data = {}

    for index, row in db.iterrows():
        if row['lista pub'] == 's':
            valor_ramal = str(row["ramal"])

            if len(valor_ramal) > 4 :
                valor_ramal = valor_ramal[:-2]
            else:
                valor_ramal = valor_ramal

            if len(valor_ramal) < 4 :
                valor_ramal = f'0{valor_ramal}'
            else:
                valor_ramal = valor_ramal

            ramal_f = f"<tr><td><p><span>{row['nome_pub']}</span></p></td><td><p class=\"text-nowrap\" style=\"text-align: end;\"><span>3410 - {valor_ramal}</span></p></td></tr>"

            local_pub = row['local pub'] if pd.notna(row['Divisao']) and row['Divisao'] != "" else invisivel

            # Evitar chaves vazias no dicionário
            if local_pub not in grouped_data:
                grouped_data[local_pub] = []

            # Adiciona o ramal no subgrupo
            grouped_data[local_pub].append(ramal_f)
    # Começa a criação do HTML com a lista de grupos
    html_output = "<div style=\"text-align: center; \"><div class=\"d-flex flex-column justify-content-center align-items-center\"><table><tbody><tr><td colspan=\"2\">" \
                  "<p> </p><p class=\"text-center\" style=\"text-align: center; \"><strong>TELEFONES ÚTEIS</strong></p><p class=\"text-center\" style=\"text-align: center; \">" \
                  "<strong>HOSPITAL UNIVERSITÁRIO DA GRANDE DOURADOS<br /></strong></p><p> </p></td></tr><tr><td colspan=\"2\"><p> </p><p class=\"text-center\"><strong>" \
                  "​</strong></p></td></tr><div class=\"d-flex flex-column justify-content-center align-items-center\">"

    for local_pub, ramais in grouped_data.items():
        html_output += f"<tr><td colspan=\"2\"><p> </p><p class=\"text-center\"><strong>{local_pub}</strong></p></td></tr><table><tbody>"

        for ramal in ramais:
            html_output += ramal
        html_output += "</tbody></table>"

    html_output += "</div></tbody></table></div></div>"

    html_pub_output = html_output
    return html_pub_output


def converter_lis_organograma():
    xls = pd.ExcelFile("src/Ramais.xlsx")
    db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

    grouped_data = {}

    for index, row in db.iterrows():
        if row['lista privada'] == 's':
            valor_ramal = str(row["ramal"])
            valor_ramal = valor_ramal[:-2] if len(valor_ramal) > 4 else valor_ramal
            valor_ramal = valor_ramal.zfill(4)  # garante que tenha 4 dígitos

            ramal_f = f"<li><p><span>{row['nome']}</span><span class=\"text-nowrap\" style=\"text-align:end;\"> - {valor_ramal}</span></p></li>"

            gdsu_gerencia = row['Gerencia'] if pd.notna(row['Gerencia']) and row['Gerencia'] != "" else 'identificador_vazio_g'
            gdsu_divisao = row['Divisao'] if pd.notna(row['Divisao']) and row['Divisao'] != "" else 'identificador_vazio_d'
            gdsu_setor = row['Setor'] if pd.notna(row['Setor']) and row['Setor'] != "" else 'identificador_vazio_s'
            gdsu_unidade = row['Unidade'] if pd.notna(row['Unidade']) and row['Unidade'] != "" else 'identificador_vazio_u'

            grouped_data.setdefault(gdsu_gerencia, {}) \
                        .setdefault(gdsu_divisao, {}) \
                        .setdefault(gdsu_setor, {}) \
                        .setdefault(gdsu_unidade, []) \
                        .append(ramal_f)

    html_output = """
    <div class="mt-5"><div>
    <p style="text-align: center; "><strong>RAMAIS INTERNOS POR ORGANOGRAMA</strong></p>
    <a class="toggle">HOSPITAL UNIVERSITÁRIO DA GRANDE DOURADOS</a>
    </div><table><tbody><tr><td>
    """

    for gdsu_gerencia, divisoes in grouped_data.items():
        html_output += f"""
        <div class="d-flex flex-column">
        <a class="toggle closed">{'' if gdsu_gerencia == 'identificador_vazio_g' else gdsu_gerencia}</a>
        <div class="conteudo"><table><tbody><tr><td><ul>
        """

        for gdsu_divisao, setores in divisoes.items():
            html_output += f"""
            <div class="subNivOrganizacaoa">
            <a class="toggle closed">{'' if gdsu_divisao == 'identificador_vazio_d' else gdsu_divisao}</a>
            <div class="conteudo"><table><tbody><tr><td>
            """

            for gdsu_setor, unidades in setores.items():
                html_output += f"<p class='text-primary'>{'' if gdsu_setor == 'identificador_vazio_s' else gdsu_setor}</p><ul>"

                for gdsu_unidade, ramais in unidades.items():
                    if gdsu_unidade == 'identificador_vazio_u':
                        html_output += "<p></p>"
                    else:
                        html_output += f"<li><p class='text-primary'>{gdsu_unidade}</p><ul>"

                    for ramal in ramais:
                        html_output += ramal #ramal_f

                    html_output += "</ul> </li>" # Unidade

                html_output += "</ul>" # Setor

            html_output += "</td></tr></tbody></table></div></div>" #Divisão

        html_output += "</ul></td></tr></tbody></table></div></div>" #Gerencia

    html_output += "</td></tr></tbody></table></div>" #geral

    return html_output

def converter_lis_pesquisa():

    xls = pd.ExcelFile("src/Ramais.xlsx")
    db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

    grouped_data = {}
    html_output = "<div class=\"mt-5 ms-n1\"><p style=\"text-align: center; column-span: 2;\"><strong>        LISTA COMPLETA DE RAMAIS</strong></p><p style=\"text-align: center; column-span: 2\">        Para pesquisar, expanda a lista e pressione 'Ctrl' + 'F'</p><a class=\"toggle closed\">EXIBIR TODOS OS RAMAIS</a><div class=\"conteudo\"><div class=\"d-flex justify-content-center\"><table><tbody>"
    
    for index, row in db.iterrows():
        if row['lista privada'] == 's':
        
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
            gdsu_unidade = row['Unidade'] if pd.notna(row['Unidade']) and row['Unidade'] != "" else 'identificador_vazio_u'
    
            if gdsu_unidade not in grouped_data:
                grouped_data[gdsu_unidade] = [] 
    
            # Adiciona o ramal no subgrupo
            grouped_data[gdsu_unidade].append(ramal_f)
    
    # Começa a criação do HTML com a lista de grupos
    
    for gdsu_unidade, ramais in grouped_data.items():
        html_output += f"<tr><td colspan=\"2\"><p class=\"text-center\"><strong>{'' if gdsu_unidade == 'identificador_vazio_u' else gdsu_unidade}</strong></p></td></tr>"
    
        for ramal in ramais:
            html_output += ramal  # Adiciona os ramais na lista do grupo
    
    html_output += "</tbody></table></div></div></div>"  # fecha a tag das unidades
    html_lis_output = html_output
    
    return html_lis_output

def converter(label_converter):
    output_cnv_html = f'{converter_lis_pub()}{converter_lis_organograma()}{converter_lis_pesquisa()}'
    label_converter.setText(output_cnv_html)