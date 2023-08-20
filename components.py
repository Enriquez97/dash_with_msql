import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import dcc, html

def loadingOverlay(children = [],type="bars",colors="#01414b",size="xl"):
        return html.Div(dmc.LoadingOverlay(children,loaderProps={"variant": type, "color": colors, "size": size}))

def select(
        id='',texto='',place="Todos",value=None,data=[],clearable=False, searchable = False, size='md'
    ):
        return  html.Div(
            dmc.Select(
                id=id,
                data = data,
                label = texto,
                clearable = clearable,
                placeholder = place,
                style = {'font-size': "90%"},
                value = value,
                size = size,
                searchable = searchable

            )
)
        
def multiSelect(
        id='w',texto='',place="",value=None,data=[],size='xs'):
        return html.Div(
            dmc.MultiSelect(
                        #data=["React", "Angular", "Svelte", "Vue"],
                        id=id,
                        label=texto,
                        placeholder=place,
                        searchable=True,
                        nothingFound="Opción no encontrada",
                        value=value,
                        data=data,
                        style={'font-size': "80%"},
                        size=size, 
                    )
        ) 
        
def Column(content=[],size=12):
      return dbc.Col(content,width=size,className=f"col-xl-{size} col-md-{size} col-sm-12 col-12 mb-1",style={'padding-left': '7px','padding-right': '10px'})

def Row(content=[]):
    return dbc.Row(content)

def Div(content=[],id='', style = {}):
    return html.Div(children=content,id=id, style = style)