from imports import pd
import unicodedata

def normalizar(texto):
    if pd.isna(texto):
        return ''
    return unicodedata.normalize('NFKD', str(texto)).encode('ASCII', 'ignore').decode('utf-8').lower()

def buscar(local, input_valueSearch, label_SearchTextArea):
    xls = pd.ExcelFile("src/Ramais.xlsx")
    db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

    try:
        if local == 'id' or local == 'ramal':
            busca = int(input_valueSearch.text())
            pesquisa = db.loc[db[local] == busca]
        else:
            busca = normalizar(input_valueSearch.text())

            # Normaliza a coluna selecionada
            coluna_normalizada = db[local].apply(normalizar)

            # Busca parcial usando str.contains
            pesquisa = db.loc[coluna_normalizada.str.contains(busca, na=False)]

        if not pesquisa.empty:
            ramais_info = ""
            for index, row in pesquisa.iterrows():
                if row['lista privada'] == 's' and row['lista pub'] == 's':
                    status_ramal = 'interno e externo'
                elif row['lista privada'] == 's' and row['lista pub'] == 'n':
                    status_ramal = 'interno'
                elif row['lista privada'] == 'n' and row['lista pub'] == 's':
                    status_ramal = 'externo'
                else:
                    status_ramal = 'não exibir'

                if row['type'] == 'P':
                    nome_ramal = row['nome']
                elif row['type'] == 'F':
                    nome_ramal = f"FILA - {row['nome']}"
                else:
                    nome_ramal = 'erro no nome ou tipo do ramal'

                if local == 'id' or local == 'ramal':
                    if row['type'] == 'P':
                        type = 'Principal'
                    elif row['type'] == 'F':
                        type = 'Fila'
                    else:
                        type = 'Erro'

                    divisao = row['Divisao'] if row['Divisao'] else ""
                    setor = row['Setor'] if row['Setor'] else ""

                    gdsu = f"  ->{row['Gerencia']}\n      ->{divisao}\n       ->{setor}\n        ->{row['Unidade']} "

                    nome_publico = row['nome_pub'] if row['nome_pub'] else ""
                    nome_pub = f'nome simplificado (aparece só na lista publica/externa): {nome_publico} \n' if nome_publico else ""

                    ramais_info += (
                        f"ID: {row['id']} \nnome: {nome_ramal} \n{nome_pub}Ramal: {row['ramal']:.0f} \n"
                        f"  Responsável: {row['responsavel']} \n{gdsu} \n  Tipo: {type} \n  Incluir: {status_ramal} \n"
                        f"  Ultima atualização: {row['ultima atualização']} \n    {row['ultima modificação']} \n"
                    )
                else:
                    ramais_info += f"ID: {row['id']}, nome: {nome_ramal}, Ramal: {row['ramal']:.0f}, Status: {status_ramal}\n"

            label_SearchTextArea.setText(ramais_info)
        else:
            label_SearchTextArea.setText("Nenhum ramal encontrado.")

    except:
        label_SearchTextArea.setText(f"Erro ao validar os dados")


def editar(collumn, id, value, input_valueEdit, label_EditTextArea):
    xls = pd.ExcelFile("src/Ramais.xlsx")
    db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

    try:
# If the local of search is 'id' ou 'ramal', change the type of the value to integer, if not, set string on the type of value.
        if collumn == 'ramal':
            value = int(input_valueEdit.text())
        else:
            value = input_valueEdit.text()
        label_EditTextArea.setText(f"Na coluna {collumn}, linha {id}, o valor foi alterado para {value}")
        db.loc[db['id'] == id, collumn] = value #set the new value
    except:
        label_EditTextArea.setText("insira um valor válido (Um número de 4 dígitos inteiro)")
    
    db.to_excel('src/Ramais.xlsx', index=False) # Save the changes

def dados_adc(new_id, new_ramal, new_name, new_resp, new_gdsu_g, new_gdsu_d, new_gdsu_s, new_gdsu_u, new_priv_list, new_pub_list, new_local_pub, new_nome_pub, new_type, new_upd_date, new_upd_mod, label_EditTextArea):
    try:
        ramal = int(new_ramal)
    except:
        label_EditTextArea.setText(f"Erro: insira um ramal") #check if there is a ramal, becouse if only mandatory value

    if new_name == '':
        name = 'Sem nome'
    else:
        name = new_name

    if new_nome_pub == '':
        name_pub = ''
    else:
        name_pub = new_nome_pub
    
    if new_resp == '':
        resp = 'Sem responsável'
    else:
        resp = new_resp
    
    if new_gdsu_g == '':
        gdsu_g = 'SEM GERENCIA'
    else:
        gdsu_g = new_gdsu_g.upper()

    if new_gdsu_d == '':
        gdsu_d = 'SEM DIVISÃO'
    else:
        gdsu_d = new_gdsu_d.upper()

    if new_gdsu_s == '':
        gdsu_s = 'SEM SETOR'
    else:
        gdsu_s = new_gdsu_s.upper()

    if new_gdsu_u == '':
        gdsu_u = 'SEM UNIDADE'
    else:
        gdsu_u = new_gdsu_u.upper()

    if new_priv_list == '':
        priv_list = 'n'
    else:
        priv_list = new_priv_list

    if new_pub_list == '':
        pub_list = 'n'
    else:
        pub_list = new_pub_list

    if new_local_pub == '':
        local_pub = ''
    else:
        local_pub = new_local_pub
    
    if new_type == '':
        tipo = 'P'
    else:
        tipo = new_type
    
    if new_upd_date == '':
        upd_date = 'aaaa/mm/dd 00:00:00'
    else:
        upd_date = new_upd_date
    
    if new_upd_mod == '':
        upd_mod = 'Incluso na lista'
    else:
        upd_mod = new_upd_mod
# Create a object with all the informations
    ramal_novo = pd.DataFrame({
                'id': [new_id],
                'ramal': [ramal],
                'nome': [name],
                'responsavel': [resp],
                'Gerencia': [gdsu_g],
                'Divisao': [gdsu_d],
                'Setor': [gdsu_s],
                'Unidade': [gdsu_u],
                'lista privada': [priv_list],
                'lista pub':[pub_list],
                'type':[tipo],
                'local pub':[local_pub],
                'nome_pub': [name_pub],
                'ultima atualização':[upd_date],
                'ultima modificação':[upd_mod]
            })
#return the object
    return ramal_novo

def adicionar(new_ramal, new_name, new_resp, new_gdsu_g, new_gdsu_d, new_gdsu_s, new_gdsu_u, new_priv_list, new_pub_list, new_local_pub, new_nome_pub, new_type, new_upd_date, new_upd_mod, label_EditTextArea):
    xls = pd.ExcelFile("src/Ramais.xlsx")
    db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
#create a new id
    total_id = int(db['id'].nunique())
    new_id = total_id + 1

    if db is not None:
        #create the object 'ramal novo' with the funciton 'dados_adc', that return the object 'ramal_novo'
        ramal_novo = dados_adc(new_id, new_ramal, new_name, new_resp, new_gdsu_g, new_gdsu_d, new_gdsu_s, new_gdsu_u, new_priv_list, new_pub_list, new_local_pub, new_nome_pub, new_type, new_upd_date, new_upd_mod, label_EditTextArea)
        #Concatenating the DBs
        db = pd.concat([db, ramal_novo], ignore_index=True)
        
        response = f'O ramal {str(new_ramal)} foi adicionado com o id {str(new_id)}'
    else:
        response = 'Erro: não foi possível adicionar o Ramal'

    try:
        db.to_excel('src/Ramais.xlsx', index=False) #Save the new ramal in db
    except:
        response = 'Erro: não foi possível salvar'
    
    label_EditTextArea.setText(response)

def deletar(id, label_EditTextArea):
    xls = pd.ExcelFile("src/Ramais.xlsx")
    db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

    try:
        index = id-1

        db = db.drop(index=index)
        db = db.reset_index(drop=True) #reseta todos os IDs
        db['id'] = db.index + 1 #gera todos os IDs novamente de modo procedural
        label_EditTextArea.setText(f"o Ramal foi deletado")
        db.to_excel('src/Ramais.xlsx', index=False)
    except:
        label_EditTextArea.setText('Erro: id inexistente')