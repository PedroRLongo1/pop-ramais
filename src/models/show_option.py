from imports import QTableWidget, QTableWidgetItem
import pandas as pd

def show_option_pesquisa(opcao_panel, widget_panelDownSearch, widget_panelDownMods, widget_panelDownConvert):
    opcao_panel.setText(f"Modo: Busca")
    widget_panelDownSearch.setVisible(True)  # Set visible to Widget
    widget_panelDownMods.setVisible(False)  # Set invisible to Widget
    widget_panelDownConvert.setVisible(False)  # Set invisible to Widget

def show_option_editar(opcao_panel, widget_panelDownSearch, widget_panelDownMods, widget_panelDownConvert):
    opcao_panel.setText(f"Modo: Edição")
    widget_panelDownSearch.setVisible(False)   # Set invisible to Widget
    widget_panelDownMods.setVisible(True)  #Set visible to Widget
    widget_panelDownConvert.setVisible(False)  # Set invisible to Widget

def show_option_converter(opcaoPainel, widget_panelDownSearch, widget_panelDownMods, widget_panelDownConvert):
    opcaoPainel.setText(f"Modo: Conversão")
    widget_panelDownSearch.setVisible(False)  # Set invisible to Widget
    widget_panelDownMods.setVisible(False)  #Set invisible to Widget
    widget_panelDownConvert.setVisible(True)# Set visible to Widget

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