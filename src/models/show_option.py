from imports_pyside import *
import pandas as pd

def show_option_pesquisa(opcao_panel, widget_panelDownSearch, widget_panelDownEdit, widget_panelDownConvert):
    opcao_panel.setText(f"Modo: Busca")
    widget_panelDownSearch.setVisible(True)  # Set visible to Widget
    widget_panelDownEdit.setVisible(False)  # Set invisible to Widget
    widget_panelDownConvert.setVisible(False)  # Set invisible to Widget

def show_option_editar(opcao_panel, widget_panelDownSearch, widget_panelDownEdit, widget_panelDownConvert):
    opcao_panel.setText(f"Modo: Edição")
    widget_panelDownSearch.setVisible(False)   # Set invisible to Widget
    widget_panelDownEdit.setVisible(True)  #Set visible to Widget
    widget_panelDownConvert.setVisible(False)  # Set invisible to Widget

def show_option_converter(opcaoPainel, p_d_pesquisa_widget, p_d_editar_widget, p_d_conversao_widget):
    opcaoPainel.setText(f"Modo: Conversão")
    p_d_pesquisa_widget.setVisible(False)  # Set invisible to Widget
    p_d_editar_widget.setVisible(False)  #Set invisible to Widget
    p_d_conversao_widget.setVisible(True)# Set visible to Widget

def atualiza_tabela(table):

    xls = pd.ExcelFile("src/Ramais.xlsx")
    db = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

    table.setRowCount(0)
    table.setColumnCount(len(db.columns))

    for row in range(len(db)):
        table.insertRow(row)
        for col in range(len(db.columns)):
            item = QTableWidgetItem(str(db.iloc[row, col]))
            table.setItem(row, col, item)