from imports import *

xls = pd.ExcelFile("src/Ramais.xlsx")
db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

from models.show_option import show_option_editar, show_option_pesquisa, show_option_converter, atualiza_tabela
from models.actions import buscar, editar, adicionar, deletar
from models.conversor import  converter, copy_html

class Project(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Gerenciador de ramais')
        self.setGeometry(0, 0, 1800, 1000)

        self.splitter = QSplitter(Qt.Horizontal)

        self.layout_main = QHBoxLayout()

        # painel {
        #painel up {
        self.layout_painel_up = QVBoxLayout()
        self.painel_up_widget = QWidget()
        self.painel_up_widget.setObjectName("painelUp")
        self.painel_up_widget.setLayout(self.layout_painel_up)

        self.buttonPesquisa = QPushButton("pesquisar")
        self.buttonPesquisa.setObjectName("buttonPesquisa")
        self.buttonPesquisa.clicked.connect(self.show_pesquisa)

        self.buttonEdit = QPushButton("Editar")
        self.buttonEdit.setObjectName("buttonEdit")
        self.buttonEdit.clicked.connect(self.show_editar)

        self.buttonConvert = QPushButton("Converter")
        self.buttonConvert.setObjectName("buttonConvert")
        self.buttonConvert.clicked.connect(self.show_converter)

        self.opcaoPainel = QLabel("selecione a função")
        self.opcaoPainel.setObjectName("opcaoPainel")

        self.layout_botoes = QHBoxLayout()
        self.layout_botoes.addWidget(self.buttonPesquisa)
        self.layout_botoes.addWidget(self.buttonEdit)
        self.layout_botoes.addWidget(self.buttonConvert)
        self.layout_botoes.addWidget(self.opcaoPainel)

        self.layout_painel_up.addLayout(self.layout_botoes)

        # painel down
        self.layout_painel_down = QVBoxLayout()
        self.painel_down_widget = QWidget()
        self.painel_down_widget.setObjectName("painelDown")
        self.painel_down_widget.setLayout(self.layout_painel_down)

        # p_d_pesquisa (painel de pesquisa)
        self.layout_p_d_pesquisa = QVBoxLayout()
        self.p_d_pesquisa_widget = QWidget()
        self.p_d_pesquisa_widget.setObjectName("p_d_pesquisa")
        self.p_d_pesquisa_widget.setLayout(self.layout_p_d_pesquisa)

        self.input_local = QComboBox()
        self.input_local.setObjectName("input_pd")

        col_disp_pesquisa = ['id', 'ramal', 'nome', 'responsavel', 'Gerencia', 'Divisao', 'Setor', 'Unidade', 'lista privada', 'lista pub', 'type', 'local pub', 'nome_pub', 'ultima atualização', 'ultima modificação']
        self.input_local.addItems(col_disp_pesquisa)

        self.input_local.setObjectName("input_pd")
        
        self.input_value_search = QLineEdit(placeholderText="O que será procurado?")
        self.input_value_search.setObjectName("input_pd")
        self.button_buscar_search = QPushButton("Buscar")
        self.button_buscar_search.setObjectName("button_search")
        self.button_buscar_search.clicked.connect(self.call_buscar)

        # text area
        self.text_area = QLabel("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        self.text_area.setObjectName("text_area")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.text_area)
        self.scroll_area.setWidgetResizable(True)  # Permite que o widget seja redimensionado com a área de rolagem

        self.layout_p_d_pesquisa.addWidget(self.scroll_area)

        self.layout_p_d_pesquisa.addWidget(self.input_local)
        self.layout_p_d_pesquisa.addWidget(self.input_value_search)
        self.layout_p_d_pesquisa.addWidget(self.button_buscar_search)
        self.layout_p_d_pesquisa.addWidget(self.scroll_area)
        

        # p_d_editar (painel de editar)
        self.layout_p_d_editar = QVBoxLayout()
        self.p_d_editar_widget = QWidget()
        self.p_d_editar_widget.setObjectName("p_d_editar")
        self.p_d_editar_widget.setLayout(self.layout_p_d_editar)

        # Substituindo QLineEdit por QComboBox
        self.input_collumn = QComboBox()
        self.input_collumn.setObjectName("input_pd")

        # Adicionando opções de colunas
        col_disp_editar = ['ramal', 'nome', 'responsavel', 'Gerencia', 'Divisao', 'Setor', 'Unidade', 'lista privada', 'lista pub', 'type', 'local pub', 'nome_pub', 'ultima atualização', 'ultima modificação']  # Colunas que o usuário pode escolher
        self.input_collumn.addItems(col_disp_editar)

        self.input_row = QLineEdit(placeholderText="qual o id do item?")
        self.input_row.setObjectName("input_pd")
        self.input_value_edit = QLineEdit(placeholderText="qual o valor a ser substituido?")
        self.input_value_edit.setObjectName("input_pd")
        self.button_buscar_edit = QPushButton("atualizar")
        self.button_buscar_edit.setObjectName("button_edit")
        self.button_buscar_edit.clicked.connect(self.call_editar)

        self.label_avisos_editar = QLabel("")
        self.label_avisos_editar.setObjectName("label_avisos")

        # Adicionando widgets ao layout de editar
        self.layout_p_d_editar.addWidget(self.input_collumn)
        self.layout_p_d_editar.addWidget(self.input_row)
        self.layout_p_d_editar.addWidget(self.input_value_edit)
        self.layout_p_d_editar.addWidget(self.button_buscar_edit)


        # painel deletar
        self.layout_p_d_delete = QVBoxLayout()
        self.p_d_delete_widget = QWidget()
        self.p_d_delete_widget.setObjectName("p_d_delete")
        self.p_d_delete_widget.setLayout(self.layout_p_d_delete)

        self.input_id_del = QLineEdit(placeholderText="qual o id do item?")
        self.input_id_del.setObjectName("input_del")
        self.button_del = QPushButton("deletar")
        self.button_del.setObjectName("button_del")
        self.button_del.clicked.connect(self.call_del)

        self.layout_p_d_delete.addWidget(self.input_id_del)
        self.layout_p_d_delete.addWidget(self.button_del)

        # painel adicionar
        self.layout_p_d_add = QVBoxLayout()
        self.p_d_add_widget = QWidget()
        self.p_d_add_widget.setObjectName("p_d_add")
        self.p_d_add_widget.setLayout(self.layout_p_d_add)

        self.input_new_ramal = QLineEdit(placeholderText="qual o ramal")
        self.input_new_ramal.setObjectName("input_add")
        self.input_new_nome = QLineEdit(placeholderText="qual o nome")
        self.input_new_nome.setObjectName("input_add")
        self.input_new_resp = QLineEdit(placeholderText="qual o responsável")
        self.input_new_resp.setObjectName("input_add")
        self.input_new_gdsu_g = QLineEdit(placeholderText="em qual gerência se localiza?")
        self.input_new_gdsu_g.setObjectName("input_add")
        self.input_new_gdsu_d = QLineEdit(placeholderText="em qual divisão se localiza?")
        self.input_new_gdsu_d.setObjectName("input_add")
        self.input_new_gdsu_s = QLineEdit(placeholderText="em qual setor se localiza?")
        self.input_new_gdsu_s.setObjectName("input_add")
        self.input_new_gdsu_u = QLineEdit(placeholderText="em qual unidade se localiza?")
        self.input_new_gdsu_u.setObjectName("input_add")
        self.input_new_lis_pri = QLineEdit(placeholderText="deve aparecer na lista interna? (s/n)")
        self.input_new_lis_pri.setObjectName("input_add")
        self.input_new_lis_pub = QLineEdit(placeholderText="deve aparecer na lista publica? (s/n)")
        self.input_new_lis_pub.setObjectName("input_add")
        self.input_new_type = QLineEdit(placeholderText="O ramal é do tipo Fila? (s/n)")
        self.input_new_type.setObjectName("input_add")
        self.input_new_local_pub = QLineEdit(placeholderText="localização na lista publica (Necessário apenas se aparecer na lista pública)")
        self.input_new_local_pub.setObjectName("input_add")
        self.input_new_name_pub = QLineEdit(placeholderText="nome na lista publica (Necessário apenas se aparecer na lista pública)")
        self.input_new_name_pub.setObjectName("input_add")
        self.input_new_update_date = QLineEdit(placeholderText="data e hora")
        self.input_new_update_date.setObjectName("input_add")
        self.input_new_update_mod = QLineEdit(placeholderText="o que foi feito?")
        self.input_new_update_mod.setObjectName("input_add")
        self.button_add = QPushButton("adicionar")
        self.button_add.setObjectName("button_add")
        self.button_add.clicked.connect(self.call_add)

        self.layout_p_d_add.addWidget(self.input_new_ramal)
        self.layout_p_d_add.addWidget(self.input_new_nome)
        self.layout_p_d_add.addWidget(self.input_new_resp)
        self.layout_p_d_add.addWidget(self.input_new_gdsu_g)
        self.layout_p_d_add.addWidget(self.input_new_gdsu_d)
        self.layout_p_d_add.addWidget(self.input_new_gdsu_s)
        self.layout_p_d_add.addWidget(self.input_new_gdsu_u)
        self.layout_p_d_add.addWidget(self.input_new_lis_pri)
        self.layout_p_d_add.addWidget(self.input_new_lis_pub)
        self.layout_p_d_add.addWidget(self.input_new_type)
        self.layout_p_d_add.addWidget(self.input_new_local_pub )
        self.layout_p_d_add.addWidget(self.input_new_name_pub)
        self.layout_p_d_add.addWidget(self.input_new_update_date)
        self.layout_p_d_add.addWidget(self.input_new_update_mod)
        self.layout_p_d_add.addWidget(self.button_add)

        self.layout_p_d_editar.addWidget(self.p_d_add_widget)
        self.layout_p_d_editar.addWidget(self.p_d_delete_widget)
        self.layout_p_d_editar.addWidget(self.label_avisos_editar)

        # painel_conversão
        self.layout_painel_conversao = QVBoxLayout()
        self.p_d_conversao_widget = QWidget()
        self.p_d_conversao_widget.setLayout(self.layout_painel_conversao)
        self.p_d_conversao_widget.setObjectName("painel_conversao")


        self.button_converter = QPushButton("converter para HTML")
        self.button_converter.clicked.connect(self.call_converter)
        self.button_converter.setObjectName("button_convert")
        self.button_copy_html = QPushButton("copiar")
        self.button_copy_html.clicked.connect(self.call_copy_html)
        self.button_copy_html.setObjectName("button_copy_html")

        self.label_converter = QLabel(">")
        self.label_converter.setObjectName("label_convert")
        self.scroll_convert = QScrollArea()
        self.scroll_convert.setWidget(self.label_converter)
        self.scroll_convert.setWidgetResizable(True)  # Permite que o widget seja redimensionado com a área de rolagem

        self.layout_painel_conversao.addWidget(self.button_converter)
        self.layout_painel_conversao.addWidget(self.scroll_convert)
        self.layout_painel_conversao.addWidget(self.button_copy_html)


        # Adicionando widgets ao painel
        self.layout_painel_down.addWidget(self.p_d_pesquisa_widget)  # Inicialmente visível
        self.layout_painel_down.addWidget(self.p_d_editar_widget)  # Inicialmente invisível
        self.layout_painel_down.addWidget(self.p_d_conversao_widget) # Inicialmente invisível

        self.p_d_editar_widget.setVisible(False)  # Inicializa o painel de editar como invisível
        self.p_d_conversao_widget.setVisible(False)  # Inicializa o painel de conversão como invisível

        # Adicionando od paineis ao layout principal
        self.layout_painel = QVBoxLayout()
        self.layout_painel.addWidget(self.painel_up_widget)
        self.layout_painel.addWidget(self.painel_down_widget)

        # display {
        self.layout_display = QVBoxLayout()

        # tabela {
        self.table = QTableWidget()
        self.table.setObjectName("table")

        self.table.setRowCount(len(db))
        self.table.setColumnCount(len(db.columns))

        self.table.setHorizontalHeaderLabels(db.columns.tolist())

        self.layout_display.addWidget(self.table)
        # }

        # add('painel', 'display') on main {
        self.painel_widget = QWidget()
        self.painel_widget.setLayout(self.layout_painel)
        self.painel_widget.setObjectName("painel")

        self.display_widget = QWidget()
        self.display_widget.setLayout(self.layout_display)
        self.display_widget.setObjectName("display")

        self.painel_widget.setMinimumWidth(740)
        self.display_widget.setMinimumWidth(1060)

        self.splitter.addWidget(self.painel_widget)
        self.splitter.addWidget(self.display_widget)

        self.layout_main.addWidget(self.splitter)
        # }

        # Stretch {
        self.layout_painel.addStretch()

        self.setLayout(self.layout_main)

    # funções {

    def show_pesquisa(self):
        show_option_pesquisa(self.opcaoPainel, self.p_d_pesquisa_widget, self.p_d_editar_widget, self.p_d_conversao_widget)
        atualiza_tabela(self.table)

    def show_editar(self):
        show_option_editar(self.opcaoPainel, self.p_d_pesquisa_widget, self.p_d_editar_widget, self.p_d_conversao_widget)
        atualiza_tabela(self.table)

    def show_converter(self):
        show_option_converter(self.opcaoPainel, self.p_d_pesquisa_widget, self.p_d_editar_widget, self.p_d_conversao_widget)
        atualiza_tabela(self.table)

    def call_buscar(self):
        local = self.input_local.currentText()
        buscar(local, self.input_value_search, self.text_area)
        

    def call_editar(self):
        collumn = self.input_collumn.currentText()
        id = int(self.input_row.text())
        value = self.input_value_edit.text()
        editar(collumn, id, value, self.input_value_edit, self.label_avisos_editar)
        atualiza_tabela(self.table)
   
    def call_converter(self):
        converter(self.label_converter)

    def call_copy_html(self):
        copy_html(self.label_converter)

    def call_del(self):
        id = int(self.input_id_del.text())
        deletar(id, self.label_avisos_editar)
        atualiza_tabela(self.table)
        
    def call_add(self):
        
        new_ramal = self.input_new_ramal.text()
        new_name = self.input_new_nome.text()
        new_resp = self.input_new_resp.text()
        new_gdsu_g = self.input_new_gdsu_g.text()
        new_gdsu_d = self.input_new_gdsu_d.text()
        new_gdsu_s = self.input_new_gdsu_s.text()
        new_gdsu_u = self.input_new_gdsu_u.text()
        new_type = self.input_new_type.text()
        new_priv_list = self.input_new_lis_pri.text()
        new_pub_list = self.input_new_lis_pub.text()
        new_local_pub = self.input_new_local_pub.text()
        new_upd_date = self.input_new_update_date.text()
        new_upd_mod = self.input_new_update_mod.text()
        new_nome_pub = self.input_new_name_pub.text()

        self.label_avisos_editar.setText('')
        adicionar(new_ramal, new_name, new_resp, new_gdsu_g, new_gdsu_d, new_gdsu_s, new_gdsu_u, new_priv_list, new_pub_list, new_local_pub, new_nome_pub, new_type, new_upd_date, new_upd_mod, self.label_avisos_editar)
        atualiza_tabela(self.table)
    # }