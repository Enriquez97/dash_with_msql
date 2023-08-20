from dash import Dash, dcc, html, Input, Output, State,no_update,dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from data import *
from components import select, Row, Column, loadingOverlay,multiSelect
from figures import graph_line_multi_yaxes,graph_bar_horizontal, graph_pie, graph_bar_multitraces

#list_empleados = sorted(df['Empleado'].unique())
#list_linea_producto = sorted(df['Linea_Producto'].unique())

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dmc.Container([
    
    Row([
        Column([
            dmc.Center([dmc.Title(f"Revisión de Pedidos", order=1)]),
            dmc.Center([dmc.Title(f"(Dash y Mysql)", order=3)]),    
            
            
        ],size=6),
        Column([
            select(id = 'Año',texto = 'Año Pedido', data=[{'label': i, 'value': i} for i in sp_filtros()[0]], value = sp_filtros()[0][0])#
        ],size=3),
        Column([
            select(id = 'Estado',texto = 'Estado del Pedido',data=[{'label': i, 'value': i} for i in sp_filtros()[1]], value = sp_filtros()[1][-1]) 
        ],size=3)
        
    ]),
    Row([
                    Column([
                        dmc.SegmentedControl(id='Segmented-ST',
                                    
                                    data=[
                                            {"value": "Fecha_Pedido", "label": "Diario"},
                                            {"value": "Mes_Pedido", "label": "Mensual"},
                                            
                                            
                                        ],
                                    value = "Fecha_Pedido",
                                    fullWidth = True,
                                    color = 'rgb(34, 184, 207)',
                                    size = 'xs'
                                ),
                        loadingOverlay(children = dcc.Graph(id = 'Linea-ST'))
                        
                    ],size=8),
                    Column([loadingOverlay(children = dcc.Graph(id = 'Pie-Empleado-Cliente'))],size=4),
                    
     ]),
    Row([
        Column([loadingOverlay(children = dcc.Graph(id = 'Bar-Linea-Productos'))],size=6),
        Column([loadingOverlay(children = dcc.Graph(id = 'Bar-Productos'))],size=6)
    ]),
    Row([
        multiSelect(id = 'Producto',texto = 'Productos', data=[]),
        Column([loadingOverlay(children = dcc.Graph(id = 'Bar-Precio'))],size=12),
        
    ])
    
])

@app.callback(Output('Linea-ST','figure'),
              Input('Año','value'),
              Input('Estado','value'),
              Input('Segmented-ST','value'),
            )
def update_st(anio,estado,segmented):
    
    df_pedidos_st = sp_pedidos_st_totales(year = anio, estado_pedido = estado)
    if segmented =="Fecha_Pedido":
        df = df_pedidos_st.copy()
        add_titulo = "Diario"
    else:
        df = df_pedidos_st.groupby(['Mes_Pedido','Mes_num'])[['Importe Pedido','Número de Pedidos']].sum().sort_values('Mes_num', ascending = True).reset_index()
        add_titulo = "Mensual"
    return graph_line_multi_yaxes(df = df , x = segmented, y1 = 'Importe Pedido', y2 = 'Número de Pedidos', titulo = f'Importe y Cantidad de Pedidos ({add_titulo})' )
    
@app.callback(
              Output('Pie-Empleado-Cliente','figure'),
              Input('Año','value'),
              Input('Estado','value'),
            )
def update_pie_pedidos(anio,estado):
    df_pedido_cliente_empleado =sp_empleado_cliente_totales( year = anio, estado_pedido = estado)
    return graph_pie(df = df_pedido_cliente_empleado,label_col='Cliente',value_col = 'Importe Pedido',title ='CLIENTES',showlegend = False, customdata=['Número de Pedidos'])
    

@app.callback(
              Output('Bar-Linea-Productos','figure'),
              Output('Bar-Productos','figure'),
              Input('Año','value'),
              Input('Estado','value'),
            )
def update_bar_pedidos(anio,estado):#
    
    df_pedidos_productos = sp_producto_total_pedido_importe(year = anio, estado_pedido = estado)
    #creando una lista de productos para el multiselect de productos
    
    
    #fig 1
    df_pedidos_linea_p = df_pedidos_productos.groupby(['Linea_Producto'])[['Importe Pedido','Número de Pedidos']].sum().sort_values('Importe Pedido',ascending=True).reset_index()
    
    figure_linea_productos = graph_bar_horizontal(df = df_pedidos_linea_p , x = 'Importe Pedido', y = 'Linea_Producto',title='LINEAS DE PRODUCTO',color_dataframe = 'Linea_Producto',custom_data = ['Número de Pedidos'],size_tickfont=14)
    
    #fig 2
    df_pedidos_productos = df_pedidos_productos.sort_values('Importe Pedido',ascending=True).head(20)
    
    figure_productos = graph_bar_horizontal(df = df_pedidos_productos , x = 'Importe Pedido', y = 'Producto',title='PRODUCTOS (TOP 20)',color_dataframe = 'Linea_Producto',custom_data = ['Linea_Producto','Número de Pedidos'])
    

    return  figure_linea_productos, figure_productos

@app.callback(
              Output('Bar-Precio','figure'),
              Output('Producto','data'),
              Input('Año','value'),
              Input('Estado','value'),
              Input('Producto','value'),
              
            )
def update_bar_pedidos_precios(anio,estado,lista_producto):
    #
    df_pedido_cliente_empleado =sp_productos_precios( year = anio, estado_pedido = estado)
    lista_productos_filtrado=[{'label': i, 'value': i} for i in sorted(df_pedido_cliente_empleado['Producto'].unique())]
    if lista_producto == None or len(lista_producto) == 0:
        df_pedido_cliente_empleado = df_pedido_cliente_empleado.copy()
    elif lista_producto != None or len(lista_producto) != 0:
        df_pedido_cliente_empleado=df_pedido_cliente_empleado[df_pedido_cliente_empleado['Producto'].isin(lista_producto)]
    df_pedido_cliente_empleado= df_pedido_cliente_empleado.groupby(['Producto']).sum().reset_index()
    
    return graph_bar_multitraces(df = df_pedido_cliente_empleado,x='Producto',y1='Precio_Compra_Producto',y2='Precio_Unitario',y_line= 'Ganancia',title_y='Precio',title='Ganancia por Producto'), lista_productos_filtrado
    
    
    
if __name__ == "__main__":
    app.run_server(debug=True)