from imports import *

def show_option_pesquisa(opcaoPainel, p_d_pesquisa_widget, p_d_editar_widget, p_d_conversao_widget):
    opcaoPainel.setText(f"Modo: Pesquisa")
    p_d_pesquisa_widget.setVisible(True)  # Torna o widget de pesquisa visível
    p_d_editar_widget.setVisible(False)  # Torna o widget de editar invisível
    p_d_conversao_widget.setVisible(False)  # Torna o widget de conversão invisível

def show_option_editar(opcaoPainel, p_d_pesquisa_widget, p_d_editar_widget, p_d_conversao_widget):
    opcaoPainel.setText(f"Modo: Editar")
    p_d_pesquisa_widget.setVisible(False)  # Torna o widget de pesquisa invisível
    p_d_editar_widget.setVisible(True)  # Torna o widget de editar visível
    p_d_conversao_widget.setVisible(False)  # Torna o widget de conversão invisível

def show_option_converter(opcaoPainel, p_d_pesquisa_widget, p_d_editar_widget, p_d_conversao_widget):
    opcaoPainel.setText(f"Modo: Converter")
    p_d_pesquisa_widget.setVisible(False)  # Torna o widget de pesquisa invisível
    p_d_editar_widget.setVisible(False)  # Torna o widget de editar invisível
    p_d_conversao_widget.setVisible(True)  # Torna o widget de conversão visível

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