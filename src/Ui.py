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
        self.layout_panelUp = QVBoxLayout()
        self.widget_panelUp = QWidget()
        self.widget_panelUp.setObjectName("widgetpanelUp")
        self.widget_panelUp.setLayout(self.layout_panelUp)
#       ]
#       settings of buttons that change the screen [
        self.button_Pesquisa = QPushButton("Buscar")
        self.button_Pesquisa.setObjectName("buttonSearch")
        self.button_Pesquisa.clicked.connect(self.show_pesquisa)

        self.button_Edit = QPushButton("Editar")
        self.button_Edit.setObjectName("buttonEdit")
        self.button_Edit.clicked.connect(self.show_editar)

        self.button_Convert = QPushButton("Converter")
        self.button_Convert.setObjectName("buttonConvert")
        self.button_Convert.clicked.connect(self.show_converter)

        self.opcao_panel = QLabel("selecione a função")
        self.opcao_panel.setObjectName("labelPanelOption")
#       ]
#       add this Widgets to panel_up [
        self.layout_botoes = QHBoxLayout()
        self.layout_botoes.addWidget(self.button_Pesquisa)
        self.layout_botoes.addWidget(self.button_Edit)
        self.layout_botoes.addWidget(self.button_Convert)
        self.layout_botoes.addWidget(self.opcao_panel)

        self.layout_panelUp.addLayout(self.layout_botoes)
#       ]
#    } end panel_up

#   panel_down {
#       general settings [
        self.layout_panelDown = QVBoxLayout()
        self.widget_panelDown = QWidget()
        self.widget_panelDown.setObjectName("widgetpanelDown")
        self.widget_panelDown.setLayout(self.layout_panelDown)
#       ]

#       panel_down(mode: edit) [
#         general settings <
        self.layout_panelDownSearch = QVBoxLayout()
        self.widget_panelDownSearch = QWidget()
        self.widget_panelDownSearch.setObjectName("widgetpanelDown")
        self.widget_panelDownSearch.setLayout(self.layout_panelDownSearch)
#         >
#         panel_down(mode: edit) Widgets <
        self.input_comboboxLocal = QComboBox()
        self.input_comboboxLocal.setObjectName("inputBase")

        collumns_display_pesquisa = ['id', 'ramal', 'nome', 'responsavel', 'Gerencia', 'Divisao', 'Setor', 'Unidade', 'lista privada', 'lista pub', 'type', 'local pub', 'nome_pub', 'ultima atualização', 'ultima modificação']
        self.input_comboboxLocal.addItems(collumns_display_pesquisa)
        
        self.input_valueSearch = QLineEdit(placeholderText="O que será procurado?")
        self.input_valueSearch.setObjectName("inputBase")
        self.button_Search = QPushButton("Buscar")
        self.button_Search.setObjectName("buttonBase")
        self.button_Search.clicked.connect(self.call_buscar)

        self.label_SearchTextArea = QLabel("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        self.label_SearchTextArea.setObjectName("labelSearchTextArea")
#         >
#         add this Widgets to panel_down <
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.label_SearchTextArea)
        self.scroll_area.setWidgetResizable(True)  # allows resizing with the mouse scroll

        self.layout_panelDownSearch.addWidget(self.scroll_area)

        self.layout_panelDownSearch.addWidget(self.input_comboboxLocal)
        self.layout_panelDownSearch.addWidget(self.input_valueSearch)
        self.layout_panelDownSearch.addWidget(self.button_Search)
        self.layout_panelDownSearch.addWidget(self.scroll_area)
#         >
#       ]
#       panel_down(mode: edit) first_part: edit values [
#         general settings <
        self.layout_panelDownEdit = QVBoxLayout()
        self.widget_panelDownEdit = QWidget()
        self.widget_panelDownEdit.setObjectName("widgetPanelDownEditar")
        self.widget_panelDownEdit.setLayout(self.layout_panelDownEdit)
#         >
#         Widgets of first_part<
        self.input_comboboxCollumn = QComboBox()
        self.input_comboboxCollumn.setObjectName("inputEditValues")

        col_disp_editar = ['ramal', 'nome', 'responsavel', 'Gerencia', 'Divisao', 'Setor', 'Unidade', 'lista privada', 'lista pub', 'type', 'local pub', 'nome_pub', 'ultima atualização', 'ultima modificação']  # Colunas que o usuário pode escolher
        self.input_comboboxCollumn.addItems(col_disp_editar)

        self.input_rowEdit = QLineEdit(placeholderText="qual o id do item?")
        self.input_rowEdit.setObjectName("inputEditValues")
        self.input_valueEdit = QLineEdit(placeholderText="qual o valor a ser substituido?")
        self.input_valueEdit.setObjectName("inputEditValues")
        self.button_buscarEdit = QPushButton("atualizar")
        self.button_buscarEdit.setObjectName("buttonEditValues")
        self.button_buscarEdit.clicked.connect(self.call_editar)

        self.label_EditTextArea = QLabel("")
        self.label_EditTextArea.setObjectName("labelEditTextArea")
#         >
#         add this Widgets to first_part<
        self.layout_panelDownEdit.addWidget(self.input_comboboxCollumn)
        self.layout_panelDownEdit.addWidget(self.input_rowEdit)
        self.layout_panelDownEdit.addWidget(self.input_valueEdit)
        self.layout_panelDownEdit.addWidget(self.button_buscarEdit)
#         >
#       ] end of first_part
#       panel_down(mode: edit) second_part: add values [
#         general_settings < 
        self.layout_panelDownAdd = QVBoxLayout()
        self.widget_panelDownAdd = QWidget()
        self.widget_panelDownAdd.setLayout(self.layout_panelDownAdd)
#         >
#         Widgets of second_part <
        self.input_newRamal = QLineEdit(placeholderText="qual o ramal")
        self.input_newRamal.setObjectName("inputEditValues")
        self.input_newNome = QLineEdit(placeholderText="qual o nome")
        self.input_newNome.setObjectName("inputEditValues")
        self.input_newResp = QLineEdit(placeholderText="qual o responsável")
        self.input_newResp.setObjectName("inputEditValues")
        self.input_newGdsuG = QLineEdit(placeholderText="em qual gerência se localiza?")
        self.input_newGdsuG.setObjectName("inputEditValues")
        self.input_newGdsuD = QLineEdit(placeholderText="em qual divisão se localiza?")
        self.input_newGdsuD.setObjectName("inputEditValues")
        self.input_newGdsuS = QLineEdit(placeholderText="em qual setor se localiza?")
        self.input_newGdsuS.setObjectName("inputEditValues")
        self.input_newGdsuU = QLineEdit(placeholderText="em qual unidade se localiza?")
        self.input_newGdsuU.setObjectName("inputEditValues")
        self.input_newLisPri = QLineEdit(placeholderText="deve aparecer na lista interna? (s/n)")
        self.input_newLisPri.setObjectName("inputEditValues")
        self.input_newLisPub = QLineEdit(placeholderText="deve aparecer na lista publica? (s/n)")
        self.input_newLisPub.setObjectName("inputEditValues")
        self.input_newType = QLineEdit(placeholderText="O ramal é do tipo Fila? (s/n)")
        self.input_newType.setObjectName("inputEditValues")
        self.input_newLocalPub = QLineEdit(placeholderText="localização na lista publica (Necessário apenas se aparecer na lista pública)")
        self.input_newLocalPub.setObjectName("inputEditValues")
        self.input_newNamePub = QLineEdit(placeholderText="nome na lista publica (Necessário apenas se aparecer na lista pública)")
        self.input_newNamePub.setObjectName("inputEditValues")
        self.input_newUpdateDate = QLineEdit(placeholderText="data e hora")
        self.input_newUpdateDate.setObjectName("inputEditValues")
        self.input_newUpdateMod = QLineEdit(placeholderText="o que foi feito?")
        self.input_newUpdateMod.setObjectName("inputEditValues")
        self.button_addNewRamal = QPushButton("adicionar")
        self.button_addNewRamal.setObjectName("buttonEditValues")
        self.button_addNewRamal.clicked.connect(self.call_add)
#         >
#         add this Widgets to second_part <
        self.layout_panelDownAdd.addWidget(self.input_newRamal)
        self.layout_panelDownAdd.addWidget(self.input_newNome)
        self.layout_panelDownAdd.addWidget(self.input_newResp)
        self.layout_panelDownAdd.addWidget(self.input_newGdsuG)
        self.layout_panelDownAdd.addWidget(self.input_newGdsuD)
        self.layout_panelDownAdd.addWidget(self.input_newGdsuS)
        self.layout_panelDownAdd.addWidget(self.input_newGdsuU)
        self.layout_panelDownAdd.addWidget(self.input_newLisPri)
        self.layout_panelDownAdd.addWidget(self.input_newLisPub)
        self.layout_panelDownAdd.addWidget(self.input_newType)
        self.layout_panelDownAdd.addWidget(self.input_newLocalPub )
        self.layout_panelDownAdd.addWidget(self.input_newNamePub)
        self.layout_panelDownAdd.addWidget(self.input_newUpdateDate)
        self.layout_panelDownAdd.addWidget(self.input_newUpdateMod)
        self.layout_panelDownAdd.addWidget(self.button_addNewRamal)
#         >
#       ] end of second_part
#       panel_down(mode: edit) tird_part: delete values [
#         global settings <
        self.layout_panelDownDelete = QVBoxLayout()
        self.widget_panelDownDelete = QWidget()
        self.widget_panelDownDelete.setLayout(self.layout_panelDownDelete)
#         >
#         Widgets of third part <
        self.input_idDelete = QLineEdit(placeholderText="qual o id do item?")
        self.input_idDelete.setObjectName("inputEditValues")
        self.button_delete = QPushButton("deletar")
        self.button_delete.setObjectName("buttonEditValues")
        self.button_delete.clicked.connect(self.call_del)
#         >
#         add this Widgets to tird_part <
        self.layout_panelDownDelete.addWidget(self.input_idDelete)
        self.layout_panelDownDelete.addWidget(self.button_delete)
#         >
#       ] end of tird_part
#       add the second_part, tird_part and label_avisos to first_part [
        self.layout_panelDownEdit.addWidget(self.widget_panelDownAdd)
        self.layout_panelDownEdit.addWidget(self.widget_panelDownDelete)
        self.layout_panelDownEdit.addWidget(self.label_EditTextArea)
#       ]
#       panel_down(mode: convert) [
#         general settings <
        self.layout_panelConvert = QVBoxLayout()
        self.widget_panelDownConvert = QWidget()
        self.widget_panelDownConvert.setLayout(self.layout_panelConvert)
#         >
#         Widgets of panel_down (mode: convert) <
        self.button_convert = QPushButton("converter para HTML")
        self.button_convert.clicked.connect(self.call_converter)
        self.button_convert.setObjectName("buttonConvertHTML")
        self.button_copy = QPushButton("copiar")
        self.button_copy.clicked.connect(self.call_copy_html)
        self.button_copy.setObjectName("buttonCopyHTML")

        self.label_convert = QLabel(">")
        self.label_convert.setObjectName("labelConvertTextArea")
        self.scroll_convert = QScrollArea()
        self.scroll_convert.setWidget(self.label_convert)
        self.scroll_convert.setWidgetResizable(True)
#         >
#         add this Widgets to panel_down (mode: convert) <
        self.layout_panelConvert.addWidget(self.button_convert)
        self.layout_panelConvert.addWidget(self.scroll_convert)
        self.layout_panelConvert.addWidget(self.button_copy)
#         >
#       ] end of panel_down (mode: convert)
#   }end of panel_down
#   Visibility settings of the 3 parts of the panel_down {
        self.layout_panelDown.addWidget(self.widget_panelDownSearch)  # Inicialmente visível
        self.layout_panelDown.addWidget(self.widget_panelDownEdit)  # Inicialmente invisível
        self.layout_panelDown.addWidget(self.widget_panelDownConvert) # Inicialmente invisível

        self.widget_panelDownEdit.setVisible(False)  # Inicializa o panel de editar como invisível
        self.widget_panelDownConvert.setVisible(False)  # Inicializa o panel de conversão como invisível
#   }
#   add the Widgets panel_up and panel_down to Panel_main_layout {
        self.layout_panel = QVBoxLayout()
        self.layout_panel.addWidget(self.widget_panelUp)
        self.layout_panel.addWidget(self.widget_panelDown)
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
#   change panel in one Widget {
        self.widget_panel = QWidget()
        self.widget_panel.setLayout(self.layout_panel)
        self.widget_panel.setObjectName("widgetPanel")

        self.widget_panel.setMinimumWidth(740)
#   }
#   change display in one Widget {
        self.widget_display = QWidget()
        self.widget_display.setLayout(self.layout_display)

        self.widget_display.setMinimumWidth(1060)

        self.splitter.addWidget(self.widget_panel)
        self.splitter.addWidget(self.widget_display)

        self.layout_main.addWidget(self.splitter)
#   }
#   Stretch {
        self.layout_panel.addStretch()

#   }
#)
#add Layout main to screen (
        self.setLayout(self.layout_main)
#)
#Functions (
#   functions of change what is in screen {
    def show_pesquisa(self):
        show_option_pesquisa(self.opcao_panel, self.widget_panelDownSearch, self.widget_panelDownEdit, self.widget_panelDownConvert)
        atualiza_tabela(self.table)

    def show_editar(self):
        show_option_editar(self.opcao_panel, self.widget_panelDownSearch, self.widget_panelDownEdit, self.widget_panelDownConvert)
        atualiza_tabela(self.table)

    def show_converter(self):
        show_option_converter(self.opcao_panel, self.widget_panelDownSearch, self.widget_panelDownEdit, self.widget_panelDownConvert)
        atualiza_tabela(self.table)
#   }
#   function of search mode {
    def call_buscar(self):
        local = self.input_comboboxLocal.currentText()
        buscar(local, self.input_valueSearch, self.label_SearchTextArea)
#   }
#   function of edit mode {
    def call_editar(self):
        collumn = self.input_comboboxCollumn.currentText()
        id = int(self.input_rowEdit.text())
        value = self.input_valueEdit.text()
        editar(collumn, id, value, self.input_valueEdit, self.label_EditTextArea)
        atualiza_tabela(self.table)

    def call_del(self):
        id = int(self.input_idDelete.text())
        deletar(id, self.label_EditTextArea)
        atualiza_tabela(self.table)
        
    def call_add(self):
        
        new_ramal = self.input_newRamal.text()
        new_name = self.input_newNome.text()
        new_resp = self.input_newResp.text()
        new_gdsu_g = self.input_newGdsuG.text()
        new_gdsu_d = self.input_newGdsuD.text()
        new_gdsu_s = self.input_newGdsuS.text()
        new_gdsu_u = self.input_newGdsuU.text()
        new_type = self.input_newType.text()
        new_priv_list = self.input_newLisPri.text()
        new_pub_list = self.input_newLisPub.text()
        new_local_pub = self.input_newLocalPub.text()
        new_upd_date = self.input_newUpdateDate.text()
        new_upd_mod = self.input_newUpdateMod.text()
        new_nome_pub = self.input_newNamePub.text()

        self.label_EditTextArea.setText('')
        adicionar(new_ramal, new_name, new_resp, new_gdsu_g, new_gdsu_d, new_gdsu_s, new_gdsu_u, new_priv_list, new_pub_list, new_local_pub, new_nome_pub, new_type, new_upd_date, new_upd_mod, self.label_EditTextArea)
        atualiza_tabela(self.table)
#   }
#   function of convert mode {
    def call_converter(self):
        converter(self.label_convert)

    def call_copy_html(self):
        copy_html(self.label_convert)
#   }
#)