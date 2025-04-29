from imports import *

def buscar(local, input_value_search, text_area):
    xls = pd.ExcelFile("src/Ramais.xlsx")
    db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

    try:
# If the local of search is 'id' ou 'ramal', change the type of the value to integer, if not, set string on the type of value.
        if local == 'id' or local == 'ramal':
            busca = int(input_value_search.text())
        else:
            busca = input_value_search.text()

        pesquisa = db.loc[db[local] == busca]

        if not pesquisa.empty:
            ramais_info = ""
            for index, row in pesquisa.iterrows():
# Config some values to the user know what means
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
# If the local is 'id' or 'ramal', return only one response, but, with all informations, if not, return many responses, but, with a little information
                if local == 'id' or local == 'ramal':
#Config the informations to return to User
                    if row['type'] == 'P':
                        type = 'Principal'
                    elif row['type'] == 'F':
                        type = 'Fila'
                    else:
                        type = 'Erro'

                    if row['lista privada'] == 's' and row['lista pub'] == 's':
                        status_ramal = 'interno e externo'
                    elif row['lista privada'] == 's' and row['lista pub'] == 'n':
                        status_ramal = 'interno'
                    elif row['lista privada'] == 'n' and row['lista pub'] == 's':
                        status_ramal = 'externo'
                    else:
                        status_ramal = 'não exibir'

                    if row['Divisao'] == "":
                        divisao = ""
                    else:
                        divisao = row['Divisao']

                    if row['Setor'] =="":
                        setor = ""
                    else:
                        setor = row['Setor']

                    gdsu = f"  ->{row['Gerencia']}\n      ->{divisao}\n       ->{setor}\n        ->{row['Unidade']} "

                    nome_publico = row['nome_pub']
                    if row['nome_pub'] is None:
                        nome_pub = ""
                    else:
                        nome_pub = f'nome simplificado (aparece só na lista publica/externa): {nome_publico} \n'
#pull the informations of the ramal in a formated message
                    ramais_info += f"ID: {row['id']} \nnome: {nome_ramal} \n{nome_pub} Ramal: {row['ramal']:.0f} \n  Responsável: {row['responsavel']} \n {gdsu} \n  Tipo: {type} \n  Incluir: {status_ramal} \n  Ultima atualização: {row['ultima atualização']} \n    {row['ultima modificação']} \n"
#pull the informations of the ramals in a formated message
                else:
                    ramais_info += f"ID: {row['id']},nome: {nome_ramal}, Ramal: {row['ramal']:.0f}, Status: {status_ramal}\n"
#show the message
            text_area.setText(ramais_info)
        else:
            text_area.setText("Nenhum ramal encontrado.")
    except:
        text_area.setText("Erro ao validar os dados")

def editar(collumn, id, value, input_value_edit, label_avisos_editar):
    xls = pd.ExcelFile("src/Ramais.xlsx")
    db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

    try:
# If the local of search is 'id' ou 'ramal', change the type of the value to integer, if not, set string on the type of value.
        if collumn == 'ramal':
            value = int(input_value_edit.text())
        else:
            value = input_value_edit.text()
        label_avisos_editar.setText(f"Na coluna {collumn}, linha {id}, o valor foi alterado para {value}")
        db.loc[db['id'] == id, collumn] = value #set the new value
    except:
        label_avisos_editar.setText("insira um valor válido (Um numero de 4 digitos inteiro)")
    
    db.to_excel('src/Ramais.xlsx', index=False) # Save the changes

def dados_adc(new_id, new_ramal, new_name, new_resp, new_gdsu_g, new_gdsu_d, new_gdsu_s, new_gdsu_u, new_priv_list, new_pub_list, new_local_pub, new_nome_pub, new_type, new_upd_date, new_upd_mod, label_avisos_editar):
    try:
        ramal = int(new_ramal)
    except:
        label_avisos_editar.setText(f"Erro: insira um ramal") #check if there is a ramal, becouse if only mandatory value

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

def adicionar(new_ramal, new_name, new_resp, new_gdsu_g, new_gdsu_d, new_gdsu_s, new_gdsu_u, new_priv_list, new_pub_list, new_local_pub, new_nome_pub, new_type, new_upd_date, new_upd_mod, label_avisos_editar):
    xls = pd.ExcelFile("src/Ramais.xlsx")
    db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
#create a new id
    total_id = int(db['id'].nunique())
    new_id = total_id + 1

    if db is not None:
        #create the object 'ramal novo' with the funciton 'dados_adc', that return the object 'ramal_novo'
        ramal_novo = dados_adc(new_id, new_ramal, new_name, new_resp, new_gdsu_g, new_gdsu_d, new_gdsu_s, new_gdsu_u, new_priv_list, new_pub_list, new_local_pub, new_nome_pub, new_type, new_upd_date, new_upd_mod, label_avisos_editar)
        #Concatenating the DBs
        db = pd.concat([db, ramal_novo], ignore_index=True)
        
        response = f'O ramal {str(new_ramal)} foi adicionado com o id {str(new_id)}'
    else:
        response = 'Erro: não foi possível adicionar o Ramal'

    try:
        db.to_excel('src/Ramais.xlsx', index=False) #Save the new ramal in db
    except:
        response = 'Erro: não foi possível salvar'
    
    label_avisos_editar.setText(response)

def deletar(id, label_avisos_editar):
    xls = pd.ExcelFile("src/Ramais.xlsx")
    db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

    try:
        index = id-1

        db = db.drop(index=index)
        db = db.reset_index(drop=True) #reseta todos os IDs
        db['id'] = db.index + 1 #gera todos os IDs novamente de modo procedural
        label_avisos_editar.setText(f"o Ramal foi Deletado")
        db.to_excel('src/Ramais.xlsx', index=False)
    except:
        label_avisos_editar.setText('Erro, id inexistente')