"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import re,pandas as pd
def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    def formatter(head):
        """Títulos en minúsculas y espacios -> guiones bajos."""
        return head.lower().replace(" ", "_")


    with open("files/input/clusters_report.txt", "r") as file:
        lineas = file.readlines()

    
    titulo_1 = re.sub(r"\s{2,}", "-", lineas[0]).strip().split("-")
    titulo_2 = re.sub(r"\s{2,}", "-", lineas[1]).strip().split("-")
    titulo_1.pop() 
    titulo_2.pop(0) 
    
    headers = [
        titulo_1[0],  
        f"{titulo_1[1]} {titulo_2[0]}",  
        f"{titulo_1[2]} {titulo_2[1]}",
        titulo_1[3], 
    ]
    headers = [formatter(h) for h in headers]

    data = pd.read_fwf(
        "files/input/clusters_report.txt",
        widths=[9, 16, 16, 80], 
        header=None,
        names=headers,
        skip_blank_lines=False,
        converters={headers[2]: lambda x: x.rstrip(" %").replace(",", ".")},
    ).iloc[4:] 

    claves = data[headers[3]]
    data = data[data[headers[0]].notna()].drop(columns=[headers[3]])
    data = data.astype({
        headers[0]: int,
        headers[1]: int,
        headers[2]: float,
    })

    keywords = []
    temp_text = ""
    for linea in claves:        
        if isinstance(linea, str): 
            if linea.endswith("."): 
                linea = linea[:-1]
            linea = re.sub(r'\s+', ' ', linea).strip()
            temp_text += linea + " "
        elif temp_text: 
            keywords.append(", ".join(re.split(r'\s*,\s*', temp_text.strip())))
            temp_text = ""
    if temp_text:
        keywords.append(", ".join(re.split(r'\s*,\s*', temp_text.strip())))

    data[headers[3]] = keywords

    return data
