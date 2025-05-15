from imports import QWidget, QSplitter, Qt, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QLabel, QScrollArea, QTableWidget
import pandas as pd

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
        self.setGeometry(0, 0, 1400, 1000)

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
        self.button_Pesquisa.setObjectName("buttonSwitchMode")
        self.button_Pesquisa.clicked.connect(self.show_pesquisa)

        self.button_Edit = QPushButton("Editar")
        self.button_Edit.setObjectName("buttonSwitchMode")
        self.button_Edit.clicked.connect(self.show_editar)

        self.button_Convert = QPushButton("Converter")
        self.button_Convert.setObjectName("buttonSwitchMode")
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
        self.title_searchMode = QLabel("Busca por ramais")
        self.title_searchMode.setObjectName("title_modes")
        self.title_searchMode.setAlignment(Qt.AlignCenter)

        self.input_comboboxLocal = QComboBox()
        self.input_comboboxLocal.setObjectName("componentBase")

        self.subtitle_searchSelector = QLabel("Filtro da pesquisa")
        self.subtitle_searchSelector.setObjectName("subtitle_modes")

        collumns_display_pesquisa = ['id', 'ramal', 'nome', 'responsavel', 'Gerencia', 'Divisao', 'Setor', 'Unidade', 'lista privada', 'lista pub', 'type', 'local pub', 'nome_pub', 'ultima atualização', 'ultima modificação']
        self.input_comboboxLocal.addItems(collumns_display_pesquisa)
        
        self.subtitle_searchInput = QLabel("Valor da pesquisa")
        self.subtitle_searchInput.setObjectName("subtitle_modes")
        self.input_valueSearch = QLineEdit(placeholderText="O que será procurado?")
        self.input_valueSearch.setObjectName("componentBase")
        self.button_Search = QPushButton("Buscar")
        self.button_Search.setObjectName("componentBase")
        self.button_Search.clicked.connect(self.call_buscar)

        self.label_SearchTextArea = QLabel("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        self.label_SearchTextArea.setObjectName("labelSearchTextArea")

        self.layout_searchSelector = QHBoxLayout()
        self.layout_searchinput = QHBoxLayout()

        self.layout_searchSelector.addWidget(self.subtitle_searchSelector)
        self.layout_searchSelector.addWidget(self.input_comboboxLocal)
        self.subtitle_searchSelector.setMaximumWidth(150)
        self.input_comboboxLocal.setMaximumWidth(260)

        self.layout_searchinput.addWidget(self.subtitle_searchInput)
        self.layout_searchinput.addWidget(self.input_valueSearch)
        self.subtitle_searchInput.setMaximumWidth(150)
        self.input_valueSearch.setMaximumWidth(260)

        
        self.button_Search.setMaximumSize(400, 35)
        self.button_Search.setMinimumSize(100, 25)

#         >
#         add this Widgets to panel_down <
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.label_SearchTextArea)
        self.scroll_area.setWidgetResizable(True)  # allows resizing with the mouse scroll

        self.layout_panelDownSearch.addWidget(self.scroll_area)

        self.layout_panelDownSearch.addWidget(self.title_searchMode)
        self.layout_panelDownSearch.addLayout(self.layout_searchSelector)
        self.layout_panelDownSearch.addLayout(self.layout_searchinput)
        self.layout_panelDownSearch.addWidget(self.button_Search, alignment=Qt.AlignCenter)
        self.layout_panelDownSearch.addWidget(self.scroll_area)
#         >
#       ]
#       panel_down [
#         general settings <
        self.layout_panelDown = QVBoxLayout()
        self.widget_panelDown = QWidget()
        self.widget_panelDown.setObjectName("widgetPanelDown")
        self.widget_panelDown.setLayout(self.layout_panelDown)
# >
#       ]
#       panel_down(mode: edit) first_part: edit values [
#         general settings <
        self.layout_panelDownEdit = QVBoxLayout()
        self.widget_panelDownEdit = QWidget()
        self.widget_panelDownEdit.setObjectName("widgetPanelDownSubDiv")
        self.widget_panelDownEdit.setLayout(self.layout_panelDownEdit)
#         >
#         Widgets of first_part<
        self.title_editMode = QLabel("Painel de edição")
        self.title_editMode.setObjectName("title_modes")
        self.title_editMode.setAlignment(Qt.AlignCenter)

        self.subtitle_EditSelector = QLabel("Filtro da edição")
        self.subtitle_EditSelector.setObjectName("subtitle_modes")
        self.input_comboboxCollumn = QComboBox()
        self.input_comboboxCollumn.setObjectName("inputBase")

        col_disp_editar = ['ramal', 'nome', 'responsavel', 'Gerencia', 'Divisao', 'Setor', 'Unidade', 'lista privada', 'lista pub', 'type', 'local pub', 'nome_pub', 'ultima atualização', 'ultima modificação']  # Colunas que o usuário pode escolher
        self.input_comboboxCollumn.addItems(col_disp_editar)

        self.subtitle_editInputId = QLabel("ID do ramal a ser editado")
        self.input_rowEdit = QLineEdit()
        self.subtitle_editInputValue = QLabel("Qual o novo valor?")
        self.input_valueEdit = QLineEdit()
        self.button_buscarEdit = QPushButton("atualizar")

        self.subtitle_editInputId.setObjectName("subtitle_modes")
        self.input_rowEdit.setObjectName("inputBase")
        self.subtitle_editInputValue.setObjectName("subtitle_modes")
        self.input_valueEdit.setObjectName("inputBase")
        self.button_buscarEdit.setObjectName("buttonBase")

        self.button_buscarEdit.clicked.connect(self.call_editar)
        self.button_buscarEdit.setMaximumSize(150, 30)
        self.button_buscarEdit.setMinimumSize(100, 25)

        self.label_EditTextArea = QLabel("")
        self.label_EditTextArea.setObjectName("labelEditTextArea")
#         >
#         add this Widgets to first_part<
        self.layout_panelDownEdit.addWidget(self.title_editMode)

        self.layout_editSelector = QHBoxLayout()

        self.subtitle_EditSelector.setMaximumWidth(150)
        self.input_comboboxCollumn.setMaximumWidth(150)
        self.layout_editSelector.addWidget(self.subtitle_EditSelector)
        self.layout_editSelector.addWidget(self.input_comboboxCollumn)

        self.layout_editInputId = QHBoxLayout()

        self.subtitle_editInputId.setMaximumWidth(150)
        self.input_rowEdit.setMaximumWidth(150)
        self.layout_editInputId.addWidget(self.subtitle_editInputId)
        self.layout_editInputId.addWidget(self.input_rowEdit)

        self.layout_editInputValue = QHBoxLayout()

        self.subtitle_editInputValue.setMaximumWidth(150)
        self.input_valueEdit.setMaximumWidth(150)
        self.layout_editInputValue.addWidget(self.subtitle_editInputValue)
        self.layout_editInputValue.addWidget(self.input_valueEdit)

        self.layout_panelDownEdit.addLayout(self.layout_editSelector)
        self.layout_panelDownEdit.addLayout(self.layout_editInputId)
        self.layout_panelDownEdit.addLayout(self.layout_editInputValue)

        self.layout_panelDownEdit.addWidget(self.button_buscarEdit, alignment=Qt.AlignCenter)
#         >
#       ] end of first_part
#       panel_down(mode: edit) second_part: add values [
#         general_settings < 
        self.layout_panelDownAdd = QVBoxLayout()
        self.widget_panelDownAdd = QWidget()
        self.widget_panelDownAdd.setObjectName('widgetPanelDownSubDiv')
        self.widget_panelDownAdd.setLayout(self.layout_panelDownAdd)
#         >
#         Widgets of second_part <
        self.title_addMode = QLabel("Painel de adição de ramais")
        self.title_addMode.setObjectName("title_modes")
        self.title_addMode.setAlignment(Qt.AlignCenter)

        self.subtitle_addRamal = QLabel("Insira o ramal:")
        self.subtitle_addRamal.setObjectName("subtitle_modes")
        self.input_newRamal = QLineEdit()
        self.input_newRamal.setObjectName("inputBase")
        self.layout_addRamal = QHBoxLayout()
        self.layout_addRamal.addWidget(self.subtitle_addRamal)
        self.layout_addRamal.addWidget(self.input_newRamal)
        self.subtitle_addRamal.setMaximumWidth(150)
        self.input_newRamal.setMaximumWidth(260)

        self.subtitle_addNome = QLabel("Insira o nome:")
        self.subtitle_addNome.setObjectName("subtitle_modes")
        self.input_newNome = QLineEdit()
        self.input_newNome.setObjectName("inputBase")
        self.layout_addNome = QHBoxLayout()
        self.layout_addNome.addWidget(self.subtitle_addNome)
        self.layout_addNome.addWidget(self.input_newNome)
        self.subtitle_addNome.setMaximumWidth(150)
        self.input_newNome.setMaximumWidth(260)

        self.subtitle_addResp = QLabel("Quem é o responsável:")
        self.subtitle_addResp.setObjectName("subtitle_modes")
        self.input_newResp = QLineEdit()
        self.input_newResp.setObjectName("inputBase")
        self.layout_addResp = QHBoxLayout()
        self.layout_addResp.addWidget(self.subtitle_addResp)
        self.layout_addResp.addWidget(self.input_newResp)
        self.subtitle_addResp.setMaximumWidth(150)
        self.input_newResp.setMaximumWidth(260)

        self.subtitle_addGdsuG = QLabel("Gerência:")
        self.subtitle_addGdsuG.setObjectName("subtitle_modes")
        self.input_newGdsuG = QLineEdit()
        self.input_newGdsuG.setObjectName("inputBase")
        self.layout_addGdsuG = QHBoxLayout()
        self.layout_addGdsuG.addWidget(self.subtitle_addGdsuG)
        self.layout_addGdsuG.addWidget(self.input_newGdsuG)
        self.subtitle_addGdsuG.setMaximumWidth(150)
        self.input_newGdsuG.setMaximumWidth(260)

        self.subtitle_addGdsuD = QLabel("Divisão:")
        self.subtitle_addGdsuD.setObjectName("subtitle_modes")
        self.input_newGdsuD = QLineEdit()
        self.input_newGdsuD.setObjectName("inputBase")
        self.layout_addGdsuD = QHBoxLayout()
        self.layout_addGdsuD.addWidget(self.subtitle_addGdsuD)
        self.layout_addGdsuD.addWidget(self.input_newGdsuD)
        self.subtitle_addGdsuD.setMaximumWidth(150)
        self.input_newGdsuD.setMaximumWidth(260)

        self.subtitle_addGdsuS = QLabel("Setor:")
        self.subtitle_addGdsuS.setObjectName("subtitle_modes")
        self.input_newGdsuS = QLineEdit()
        self.input_newGdsuS.setObjectName("inputBase")
        self.layout_addGdsuS = QHBoxLayout()
        self.layout_addGdsuS.addWidget(self.subtitle_addGdsuS)
        self.layout_addGdsuS.addWidget(self.input_newGdsuS)
        self.subtitle_addGdsuS.setMaximumWidth(150)
        self.input_newGdsuS.setMaximumWidth(260)

        self.subtitle_addGdsuU = QLabel("Unidade:")
        self.subtitle_addGdsuU.setObjectName("subtitle_modes")
        self.input_newGdsuU = QLineEdit()
        self.input_newGdsuU.setObjectName("inputBase")
        self.layout_addGdsuU = QHBoxLayout()
        self.layout_addGdsuU.addWidget(self.subtitle_addGdsuU)
        self.layout_addGdsuU.addWidget(self.input_newGdsuU)
        self.subtitle_addGdsuU.setMaximumWidth(150)
        self.input_newGdsuU.setMaximumWidth(260)

        self.subtitle_addLisPri = QLabel("Incluir na lista interna?")
        self.subtitle_addLisPri.setObjectName("subtitle_modes")
        self.input_newLisPri = QLineEdit(placeholderText="(s/n)")
        self.input_newLisPri.setObjectName("inputBase")
        self.layout_addLisPri = QHBoxLayout()
        self.layout_addLisPri.addWidget(self.subtitle_addLisPri)
        self.layout_addLisPri.addWidget(self.input_newLisPri)
        self.subtitle_addLisPri.setMaximumWidth(150)
        self.input_newLisPri.setMaximumWidth(260)

        self.subtitle_addLisPub = QLabel("Incluir na lista externa?")
        self.subtitle_addLisPub.setObjectName("subtitle_modes")
        self.input_newLisPub = QLineEdit(placeholderText="(s/n)")
        self.input_newLisPub.setObjectName("inputBase")
        self.layout_addLisPub = QHBoxLayout()
        self.layout_addLisPub.addWidget(self.subtitle_addLisPub)
        self.layout_addLisPub.addWidget(self.input_newLisPub)
        self.subtitle_addLisPub.setMaximumWidth(150)
        self.input_newLisPub.setMaximumWidth(260)

        self.subtitle_addType = QLabel("Faz parte de uma Fila?")
        self.subtitle_addType.setObjectName("subtitle_modes")
        self.input_newType = QLineEdit(placeholderText="(s/n)")
        self.input_newType.setObjectName("inputBase")
        self.layout_addType = QHBoxLayout()
        self.layout_addType.addWidget(self.subtitle_addType)
        self.layout_addType.addWidget(self.input_newType)
        self.subtitle_addType.setMaximumWidth(150)
        self.input_newType.setMaximumWidth(260)

        self.subtitle_addLocalPub = QLabel("Localização na lista externa:")
        self.subtitle_addLocalPub.setObjectName("subtitle_modes")
        self.input_newLocalPub = QLineEdit(placeholderText="(Necessário apenas se aparecer na lista pública)")
        self.input_newLocalPub.setObjectName("inputBase")
        self.layout_addLocalPub = QHBoxLayout()
        self.layout_addLocalPub.addWidget(self.subtitle_addLocalPub)
        self.layout_addLocalPub.addWidget(self.input_newLocalPub)
        self.subtitle_addLocalPub.setMaximumWidth(150)
        self.input_newLocalPub.setMaximumWidth(260)

        self.subtitle_addNomePub = QLabel("Nome na lista externa:")
        self.subtitle_addNomePub.setObjectName("subtitle_modes")
        self.input_newNamePub = QLineEdit(placeholderText="(Necessário apenas se aparecer na lista pública)")
        self.input_newNamePub.setObjectName("inputBase")
        self.layout_addNomePub = QHBoxLayout()
        self.layout_addNomePub.addWidget(self.subtitle_addNomePub)
        self.layout_addNomePub.addWidget(self.input_newNamePub)
        self.subtitle_addNomePub.setMaximumWidth(150)
        self.input_newNamePub.setMaximumWidth(260)

        self.subtitle_addUpdateDate = QLabel("Data de adição:")
        self.subtitle_addUpdateDate.setObjectName("subtitle_modes")
        self.input_newUpdateDate = QLineEdit(placeholderText="dd-mm-aa")
        self.input_newUpdateDate.setObjectName("inputBase")
        self.layout_addUpdateDate = QHBoxLayout()
        self.layout_addUpdateDate.addWidget(self.subtitle_addUpdateDate)
        self.layout_addUpdateDate.addWidget(self.input_newUpdateDate)
        self.subtitle_addUpdateDate.setMaximumWidth(150)
        self.input_newUpdateDate.setMaximumWidth(260)

        self.subtitle_addUpdateMod = QLabel("Alteração")
        self.subtitle_addUpdateMod.setObjectName("subtitle_modes")
        self.input_newUpdateMod = QLineEdit("Incluso na lista")
        self.input_newUpdateMod.setObjectName("inputBase")
        self.layout_addUpdateMod = QHBoxLayout()
        self.layout_addUpdateMod.addWidget(self.subtitle_addUpdateMod)
        self.layout_addUpdateMod.addWidget(self.input_newUpdateMod)
        self.subtitle_addUpdateMod.setMaximumWidth(150)
        self.input_newUpdateMod.setMaximumWidth(260)

        self.button_addNewRamal = QPushButton("Criar Ramal")
        self.button_addNewRamal.setObjectName("buttonBase")
        self.button_addNewRamal.clicked.connect(self.call_add)
        self.button_addNewRamal.setMaximumSize(200, 35)
        self.button_addNewRamal.setMinimumSize(100, 25)
#         >
#         add this Widgets to second_part <
        self.layout_panelDownAdd.addWidget(self.title_addMode)
        self.layout_panelDownAdd.addLayout(self.layout_addRamal)
        self.layout_panelDownAdd.addLayout(self.layout_addNome)
        self.layout_panelDownAdd.addLayout(self.layout_addResp)
        self.layout_panelDownAdd.addLayout(self.layout_addGdsuG)
        self.layout_panelDownAdd.addLayout(self.layout_addGdsuD)
        self.layout_panelDownAdd.addLayout(self.layout_addGdsuS)
        self.layout_panelDownAdd.addLayout(self.layout_addGdsuU)
        self.layout_panelDownAdd.addLayout(self.layout_addLisPri)
        self.layout_panelDownAdd.addLayout(self.layout_addLisPub)
        self.layout_panelDownAdd.addLayout(self.layout_addType)
        self.layout_panelDownAdd.addLayout(self.layout_addLocalPub)
        self.layout_panelDownAdd.addLayout(self.layout_addNomePub)
        self.layout_panelDownAdd.addLayout(self.layout_addUpdateDate)
        self.layout_panelDownAdd.addLayout(self.layout_addUpdateMod)
        self.layout_panelDownAdd.addWidget(self.button_addNewRamal, alignment=Qt.AlignCenter)
#         >
#       ] end of second_part
#       panel_down(mode: edit) tird_part: delete values [
#         global settings <
        self.layout_panelDownDelete = QVBoxLayout()
        self.widget_panelDownDelete = QWidget()
        self.widget_panelDownDelete.setObjectName('widgetPanelDownSubDiv')
        self.widget_panelDownDelete.setLayout(self.layout_panelDownDelete)
#         >
#         Widgets of third part <
        self.title_deleteMode = QLabel("Painel de remoção de ramais")
        self.title_deleteMode.setObjectName("title_modes")
        self.title_deleteMode.setAlignment(Qt.AlignCenter)

        self.input_idDelete = QLineEdit(placeholderText="qual o id do item?")
        self.input_idDelete.setObjectName("inputBase")
        self.button_delete = QPushButton("deletar")
        self.button_delete.setObjectName("buttonBase")
        self.button_delete.clicked.connect(self.call_del)
#         >
#         add this Widgets to tird_part <
        self.layout_panelDownDelete.addWidget(self.title_deleteMode)
        self.layout_panelDownDelete.addWidget(self.input_idDelete)
        self.layout_panelDownDelete.addWidget(self.button_delete)
#         >
#       ] end of tird_part
#       add the second_part, tird_part and label_avisos to first_part [
        self.layout_panelDownMods = QVBoxLayout()
        self.layout_panelDownMods.addWidget(self.widget_panelDownEdit)
        self.layout_panelDownMods.addWidget(self.widget_panelDownAdd)
        self.layout_panelDownMods.addWidget(self.widget_panelDownDelete)
        self.layout_panelDownMods.addWidget(self.label_EditTextArea)

        self.widget_panelDownMods = QWidget()
        self.widget_panelDownMods.setLayout(self.layout_panelDownMods)

        self.layout_panelDown.addWidget(self.widget_panelDownMods)
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
        self.button_convert.setObjectName("buttonBase")
        self.button_copy = QPushButton("copiar")
        self.button_copy.clicked.connect(self.call_copy_html)
        self.button_copy.setObjectName("buttonBase")

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
        self.layout_panelDown.addWidget(self.widget_panelDownMods)  # Inicialmente invisível
        self.layout_panelDown.addWidget(self.widget_panelDownConvert) # Inicialmente invisível

        self.widget_panelDownSearch.setVisible(True)  # Inicializa o panel de editar como invisível
        self.widget_panelDownMods.setVisible(False)  # Inicializa o panel de Edição como invisível
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

        self.widget_panel.setMinimumWidth(500)
#   }
#   change display in one Widget {
        self.widget_display = QWidget()
        self.widget_display.setLayout(self.layout_display)

        self.widget_display.setMinimumWidth(800)

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
        show_option_pesquisa(self.opcao_panel, self.widget_panelDownSearch, self.widget_panelDownMods, self.widget_panelDownConvert)
        atualiza_tabela(self.table)

    def show_editar(self):
        show_option_editar(self.opcao_panel, self.widget_panelDownSearch, self.widget_panelDownMods, self.widget_panelDownConvert)
        atualiza_tabela(self.table)

    def show_converter(self):
        show_option_converter(self.opcao_panel, self.widget_panelDownSearch, self.widget_panelDownMods, self.widget_panelDownConvert)
        atualiza_tabela(self.table)
#   }
#   function of search mode {
    def call_buscar(self):
        local = self.input_comboboxLocal.currentText()
        buscar(local, self.input_valueSearch, self.label_SearchTextArea)
#   }
#   function of edit mode {
    def call_editar(self):
        try:
                collumn = self.input_comboboxCollumn.currentText()
                id = int(self.input_rowEdit.text())
                value = self.input_valueEdit.text()
                editar(collumn, id, value, self.input_valueEdit, self.label_EditTextArea)
                atualiza_tabela(self.table)
        except:
            self.label_EditTextArea.setText("Erro: preencha os campos")

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