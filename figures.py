import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from constans import DICT_COLORS_LINEA_PRODUCTO
from functions import create_stack_np, create_hover_custom
import pandas as pd


def graph_line_multi_yaxes(df = pd.DataFrame(), x ='',y1 = '', y2 = '', titulo = '',altura = 300, template = 'none' ):
# Create figure with secondary y-axis
    figure = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add traces
    figure.add_trace(
        go.Scatter(x=df[x], y=df[y1], name = y1),
        secondary_y=False,
    )

    figure.add_trace(
        go.Scatter(x=df[x], y=df[y2], name = y2),
        secondary_y=True,
    )

    # Add figure title
    figure.update_layout(
        title_text=f"<b>{titulo}</b>", 
        title_font_family="sans-serif", 
        title_font_color = "rgba(0, 0, 0, 0.7)",
        title_font_size = 17,
        height = altura, 
        template = template,
    )

    figure.update_xaxes(title_text=f"<b>{x}</b>")
    figure.update_yaxes(title_text=f"<b>{y1}</b>", secondary_y=False)
    figure.update_yaxes(title_text=f"<b>{y2}</b>", secondary_y=True)
    figure.update_layout(legend=dict(orientation="h",yanchor="bottom",xanchor="right",y=1.02,x=1))
    figure.update_layout(hovermode="x unified")
    figure.update_layout(margin=dict(l = 60, r = 60, b= 50, t = 90, pad = 1))
    return figure


def graph_bar_horizontal(df = pd.DataFrame(), x = '', y = '', height = 400 ,
        title = '', xaxis_title = '',yaxis_title = '', showticklabel_x = True, 
        showticklabel_y = True, template = 'plotly_white', size_tickfont = 11,
        color_dataframe = '',custom_data = [], 
    ):  
        
        figure = go.Figure()
        if len(custom_data)>0:
            custom = create_stack_np(dataframe = df, lista = custom_data)
            hover_datacustom = create_hover_custom(lista = custom_data)
        else:
            custom = []
            hover_datacustom = ""
            
        figure.add_trace(
            go.Bar(y = df[y],
                   x = df[x],   
                   text = df[x],
                   
                   orientation = 'h',
                   textposition = 'outside',
                   texttemplate =' %{text:.2s}',
                   marker_color = [DICT_COLORS_LINEA_PRODUCTO[i]for i in df[color_dataframe]],    
                   opacity=0.9,
                   name = '',
                   customdata = custom,
                   hovertemplate='<br><b>'+y+': %{y}</b><br><b>'+x+': %{x:,.2f}</b>'+hover_datacustom,
                   #hoverinfo='none',
                   hoverlabel=dict(font_size=13,bgcolor='rgba(255,255,255,0.75)',font_family="sans-serif",font_color = 'black'),
                   cliponaxis=False,
            )
        )
        
        
    
        figure.update_layout(
                template = template,
                title={'text': f"<b>{title}</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                #title_font_color="#145f82",
                xaxis_title='<b>'+xaxis_title+'</b>',
                yaxis_title='<b>'+yaxis_title+'</b>',
                legend_title="",
                #font=dict(size=15,color="black"),
                title_font_family="sans-serif", 
                title_font_size = 17,
                title_font_color = "rgba(0, 0, 0, 0.7)",
                height = height, 
                
        )
        figure.update_xaxes(tickfont=dict(size=size_tickfont),color='rgba(0, 0, 0, 0.7)',showticklabels = showticklabel_x,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
        figure.update_yaxes(tickfont=dict(size=size_tickfont),color='rgba(0, 0, 0, 0.7)',showticklabels = showticklabel_y,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
        figure.update_layout(margin=dict(l = 40, r = 40, b= 40, t = 40, pad = 1))
        
        return figure

def graph_pie(df = pd.DataFrame(),label_col = '', 
             value_col = '', title = '', textinfo = 'percent+label+value' , 
             textposition = 'inside',height = 300, showlegend = True, textfont_size = 12,customdata=[]
             
    ):
        if len(customdata)>0:
            custom = create_stack_np(dataframe = df, lista = customdata)
            hover_datacustom = create_hover_custom(lista = customdata)
        else:
            custom = []
            hover_datacustom = ""
        figure = go.Figure()
        figure.add_trace(
            go.Pie(labels=df [label_col],values=df[value_col],
                
                marker_colors = px.colors.qualitative.Prism,
                #hovertemplate='<br><b>'+label_col+': %{labels}</b><br><b>'+value_col+': %{value:,.2f}</b>'
                hoverlabel=dict(font_size=15,bgcolor="white"),
                hovertemplate = "<b>%{label}</b> <br>Porcentaje:<b> %{percent} </b></br>Importe: <b>%{value}</b><br>Porcentaje:<b> %{percent}</b>"+hover_datacustom,
                customdata= custom,
                name='',
                )
        )    

        figure.update_layout(
            title={'text': f"<b>{title}</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            title_font_family="sans-serif", 
            title_font_size = 18,
            title_font_color = "rgba(0, 0, 0, 0.7)",
            template ='none'
        
        )
        figure.update_traces(textposition = textposition, textinfo = textinfo)
        figure.update_traces(hoverinfo='label+percent+value', textfont_size = textfont_size,marker=dict(line=dict(color='#000000', width=1)))
        figure.update_layout(height = height,margin = dict(t=40, b=30, l=10, r=10),showlegend = showlegend)
        
        return figure
    
def graph_bar_multitraces(df = pd.DataFrame(), x = '', y1 = '', y2 = '', height = 400 ,
        y_line = '',title = '',template = 'plotly_white', title_y=''):
    figure = go.Figure()
    figure.add_trace(go.Bar(    x=df[x],
                                y=df[y1],
                                name=y1,
                                marker_color='rgb(136, 204, 238)',
                                #customdata=dict_year['year']==selected_list[-1],
                                text=df[y1],
                                textposition="outside",
                                texttemplate='%{text:,.2f}',
                                hovertemplate = '<br><b>'+x+'</b>:%{x}'+'<br><b>'+y1+'</b>: %{y:$,.2f}<br>',
                                textfont=dict(size=11)
                                ))
    figure.add_trace(go.Bar(    x=df[x],
                                y=df[y2],
                                name=y2,
                                marker_color='rgb(204, 102, 119)',
                                #customdata=dict_year['year']==selected_list[-1],
                                text=df[y2],
                                textposition="outside",
                                texttemplate='%{text:,.2f}',
                                hovertemplate = '<br><b>'+x+'</b>:%{x}'+'<br><b>'+y2+'</b>: %{y:$,.2f}<br>',
                                textfont=dict(size=11)
                                )) 
    figure.add_trace(
            go.Scatter(
                x = df[x], 
                y = df[y_line], 
                name = y_line, 
                yaxis="y2",
                text=df[y_line],
                textposition="bottom center",
                marker_color=px.colors.qualitative.Prism[1],
                hovertemplate = '<br><b>'+x+'</b>:%{x}'+'<br><b>'+y_line+'</b>: %{y:$,.2f}<br>',
                mode='lines+markers'
                ))
    figure.update_xaxes(type='category')
    figure.update_layout(
                yaxis2=dict(
                    title=f"<b>{y_line}</b>",
                    overlaying="y",
                    side="right",
                    titlefont_size=13,
                    tickfont_size=11,
                )
    )
    figure.update_layout(
            title=f"<b>{title}</b>",
            xaxis_tickfont_size=11,
            yaxis=dict(
                title=f"<b>{title_y}</b>",
                titlefont_size=13,
                tickfont_size=14,
            ),
            xaxis=dict(
                title=f"<b>{x}</b>",
                titlefont_size=13,
                tickfont_size=11,
            ),
            legend=dict(orientation="h",yanchor="bottom",xanchor="right",y=1.02,x=1),
            barmode='group',
            bargap=0.15, # gap between bars of adjacent location coordinates.0.15
            bargroupgap=0.1, # gap between bars of the same location coordinate.
            template=template,
            margin=dict(l=40,r=40,b=40,t=40),
            height = height
            
        )
    
    return figure