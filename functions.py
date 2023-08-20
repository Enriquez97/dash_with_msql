import pandas as pd
import numpy as np

def create_stack_np(dataframe = pd.DataFrame(), lista = []):
    return np.stack(tuple(dataframe[elemento] for elemento in lista),axis = -1)

def create_hover_custom(lista = []):
    string_hover = ''
    for i,element in zip(range(len(lista)),lista):
        string_hover = string_hover+'<br><b>'+element+': %{customdata['+str(i)+']}</b>'
    return string_hover
