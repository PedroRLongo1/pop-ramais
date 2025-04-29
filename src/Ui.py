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
#Create Layout main (
    def init_ui(self):
        self.setWindowTitle('Gerenciador de ramais')
        self.setGeometry(0, 0, 1800, 1000)

        self.splitter = QSplitter(Qt.Horizontal)

        self.layout_main = QHBoxLayout()
#)
#panels (
#   panel_up {
#       settings [
        self.layout_painel_up = QVBoxLayout()
        self.painel_up_widget = QWidget()
        self.painel_up_widget.setObjectName("painelUp")
        self.painel_up_widget.setLayout(self.layout_painel_up)
#       ]
#       settings of buttons that change the screen [
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
#       ]
#       add this Widgets to panel_up [
        self.layout_botoes = QHBoxLayout()
        self.layout_botoes.addWidget(self.buttonPesquisa)
        self.layout_botoes.addWidget(self.buttonEdit)
        self.layout_botoes.addWidget(self.buttonConvert)
        self.layout_botoes.addWidget(self.opcaoPainel)

        self.layout_painel_up.addLayout(self.layout_botoes)
#       ]
#    } end panel_up

#   panel_down {
#       general settings [
        self.layout_painel_down = QVBoxLayout()
        self.painel_down_widget = QWidget()
        self.painel_down_widget.setObjectName("painelDown")
        self.painel_down_widget.setLayout(self.layout_painel_down)
#       ]

#       panel_down(mode: edit) [
#         general settings <
        self.layout_p_d_pesquisa = QVBoxLayout()
        self.p_d_pesquisa_widget = QWidget()
        self.p_d_pesquisa_widget.setObjectName("p_d_pesquisa")
        self.p_d_pesquisa_widget.setLayout(self.layout_p_d_pesquisa)
#         >
#         panel_down(mode: edit) Widgets <
        self.input_local = QComboBox()
        self.input_local.setObjectName("input_pd")

        collumns_display_pesquisa = ['id', 'ramal', 'nome', 'responsavel', 'Gerencia', 'Divisao', 'Setor', 'Unidade', 'lista privada', 'lista pub', 'type', 'local pub', 'nome_pub', 'ultima atualização', 'ultima modificação']
        self.input_local.addItems(collumns_display_pesquisa)
        
        self.input_value_search = QLineEdit(placeholderText="O que será procurado?")
        self.input_value_search.setObjectName("input_pd")
        self.button_buscar_search = QPushButton("Buscar")
        self.button_buscar_search.setObjectName("button_search")
        self.button_buscar_search.clicked.connect(self.call_buscar)

        self.text_area = QLabel("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        self.text_area.setObjectName("text_area")
#         >
#         add this Widgets to panel_down <
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.text_area)
        self.scroll_area.setWidgetResizable(True)  # allows resizing with the mouse scroll

        self.layout_p_d_pesquisa.addWidget(self.scroll_area)

        self.layout_p_d_pesquisa.addWidget(self.input_local)
        self.layout_p_d_pesquisa.addWidget(self.input_value_search)
        self.layout_p_d_pesquisa.addWidget(self.button_buscar_search)
        self.layout_p_d_pesquisa.addWidget(self.scroll_area)
#         >
#       ]
#       panel_down(mode: edit) first_part: edit values [
#         general settings <
        self.layout_p_d_editar = QVBoxLayout()
        self.p_d_editar_widget = QWidget()
        self.p_d_editar_widget.setObjectName("p_d_editar")
        self.p_d_editar_widget.setLayout(self.layout_p_d_editar)
#         >
#         Widgets of first_part<
        self.input_collumn = QComboBox()
        self.input_collumn.setObjectName("input_pd")

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
#         >
#         add this Widgets to first_part<
        self.layout_p_d_editar.addWidget(self.input_collumn)
        self.layout_p_d_editar.addWidget(self.input_row)
        self.layout_p_d_editar.addWidget(self.input_value_edit)
        self.layout_p_d_editar.addWidget(self.button_buscar_edit)
#         >
#       ] end of first_part
#       panel_down(mode: edit) second_part: add values [
#         general_settings < 
        self.layout_p_d_add = QVBoxLayout()
        self.p_d_add_widget = QWidget()
        self.p_d_add_widget.setObjectName("p_d_add")
        self.p_d_add_widget.setLayout(self.layout_p_d_add)
#         >
#         Widgets of second_part <
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
#         >
#         add this Widgets to second_part <
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
#         >
#       ] end of second_part
#       panel_down(mode: edit) tird_part: delete values [
#         global settings <
        self.layout_p_d_delete = QVBoxLayout()
        self.p_d_delete_widget = QWidget()
        self.p_d_delete_widget.setObjectName("p_d_delete")
        self.p_d_delete_widget.setLayout(self.layout_p_d_delete)
#         >
#         Widgets of third part <
        self.input_id_del = QLineEdit(placeholderText="qual o id do item?")
        self.input_id_del.setObjectName("input_del")
        self.button_del = QPushButton("deletar")
        self.button_del.setObjectName("button_del")
        self.button_del.clicked.connect(self.call_del)
#         >
#         add this Widgets to tird_part <
        self.layout_p_d_delete.addWidget(self.input_id_del)
        self.layout_p_d_delete.addWidget(self.button_del)
#         >
#       ] end of tird_part
#       add the second_part, tird_part and label_avisos to first_part [
        self.layout_p_d_editar.addWidget(self.p_d_add_widget)
        self.layout_p_d_editar.addWidget(self.p_d_delete_widget)
        self.layout_p_d_editar.addWidget(self.label_avisos_editar)
#       ]
#       painel_down(mode: convert) [
#         general settings <
        self.layout_painel_conversao = QVBoxLayout()
        self.p_d_conversao_widget = QWidget()
        self.p_d_conversao_widget.setLayout(self.layout_painel_conversao)
        self.p_d_conversao_widget.setObjectName("painel_conversao")
#         >
#         Widgets of painel_down (mode: convert) <
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
        self.scroll_convert.setWidgetResizable(True)
#         >
#         add this Widgets to panel_down (mode: convert) <
        self.layout_painel_conversao.addWidget(self.button_converter)
        self.layout_painel_conversao.addWidget(self.scroll_convert)
        self.layout_painel_conversao.addWidget(self.button_copy_html)
#         >
#       ] end of panel_down (mode: convert)
#   }end of painel_down
#   Visibility settings of the 3 parts of the panel_down {
        self.layout_painel_down.addWidget(self.p_d_pesquisa_widget)  # Inicialmente visível
        self.layout_painel_down.addWidget(self.p_d_editar_widget)  # Inicialmente invisível
        self.layout_painel_down.addWidget(self.p_d_conversao_widget) # Inicialmente invisível

        self.p_d_editar_widget.setVisible(False)  # Inicializa o painel de editar como invisível
        self.p_d_conversao_widget.setVisible(False)  # Inicializa o painel de conversão como invisível
#   }
#   add the Widgets panel_up and panel_down to Panel_main_layout {
        self.layout_painel = QVBoxLayout()
        self.layout_painel.addWidget(self.painel_up_widget)
        self.layout_painel.addWidget(self.painel_down_widget)
#   }
#)
#display (
#   general settings {
        self.layout_display = QVBoxLayout()
#   }
#   table {
#       general settings [
        self.table = QTableWidget()
        self.table.setObjectName("table")

        self.table.setRowCount(len(db))
        self.table.setColumnCount(len(db.columns))

        self.table.setHorizontalHeaderLabels(db.columns.tolist())

        self.layout_display.addWidget(self.table)
#       ]
#   }
#)
#add Panel and Display Widgets to Layout main (
#   change painel in one Widget {
        self.painel_widget = QWidget()
        self.painel_widget.setLayout(self.layout_painel)
        self.painel_widget.setObjectName("painel")

        self.painel_widget.setMinimumWidth(740)
#   }
#   change display in one Widget {
        self.display_widget = QWidget()
        self.display_widget.setLayout(self.layout_display)
        self.display_widget.setObjectName("display")

        self.display_widget.setMinimumWidth(1060)

        self.splitter.addWidget(self.painel_widget)
        self.splitter.addWidget(self.display_widget)

        self.layout_main.addWidget(self.splitter)
#   }
#   Stretch {
        self.layout_painel.addStretch()

#   }
#)
#add Layout main to screen (
        self.setLayout(self.layout_main)
#)
#Functions (
#   functions of change what is in screen {
    def show_pesquisa(self):
        show_option_pesquisa(self.opcaoPainel, self.p_d_pesquisa_widget, self.p_d_editar_widget, self.p_d_conversao_widget)
        atualiza_tabela(self.table)

    def show_editar(self):
        show_option_editar(self.opcaoPainel, self.p_d_pesquisa_widget, self.p_d_editar_widget, self.p_d_conversao_widget)
        atualiza_tabela(self.table)

    def show_converter(self):
        show_option_converter(self.opcaoPainel, self.p_d_pesquisa_widget, self.p_d_editar_widget, self.p_d_conversao_widget)
        atualiza_tabela(self.table)
#   }
#   function of search mode {
    def call_buscar(self):
        local = self.input_local.currentText()
        buscar(local, self.input_value_search, self.text_area)
#   }
#   function of edit mode {
    def call_editar(self):
        collumn = self.input_collumn.currentText()
        id = int(self.input_row.text())
        value = self.input_value_edit.text()
        editar(collumn, id, value, self.input_value_edit, self.label_avisos_editar)
        atualiza_tabela(self.table)

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
#   }
#   function of convert mode {
    def call_converter(self):
        converter(self.label_converter)

    def call_copy_html(self):
        copy_html(self.label_converter)
#   }
#)