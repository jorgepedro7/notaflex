import xml.etree.ElementTree as ET
import pandas as pd
from utils.config import icms_matrix

def get_icms_rate_from_matrix(origem, destino):
    try:
        # Procurar a alíquota na matriz com origem na linha e destino na coluna
        aliquota = icms_matrix.loc[origem, destino]
        return aliquota
    except KeyError:
        return None  


def process_xml_batch(file):
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        namespaces = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

        # Identificar os estados de origem e destino
        origem_elem = root.find(".//ns:enderEmit/ns:UF", namespaces)
        destino_elem = root.find(".//ns:enderDest/ns:UF", namespaces)

        # Verificar se os elementos foram encontrados
        origem = origem_elem.text if origem_elem is not None else "Desconhecido"
        destino = destino_elem.text if destino_elem is not None else "Desconhecido"

        # Buscar a alíquota na matriz
        aliquota = get_icms_rate_from_matrix(origem, destino)

        # Buscaro número da Nota Fiscal
        nNF_elem = root.find(".//ns:ide/ns:nNF", namespaces)
        numero_nf = nNF_elem.text if nNF_elem is not None else "Desconhecido"

        if aliquota is None:
            return {"Erro": f"Alíquota não encontrada para Origem: {origem}, Destino: {destino}"}

        # Processar valores da nota
        vProd_elem = root.find(".//ns:vProd", namespaces)
        vFrete_elem = root.find(".//ns:vFrete", namespaces)
        vSeg_elem = root.find(".//ns:vSeg", namespaces)

        vProd = float(vProd_elem.text) if vProd_elem is not None else 0.0
        vFrete = float(vFrete_elem.text) if vFrete_elem is not None else 0.0
        vSeg = float(vSeg_elem.text) if vSeg_elem is not None else 0.0

        base_calculo = vProd + vFrete + vSeg
        icms = base_calculo * aliquota / 100

        # Retornar os resultados como DataFrame
        return pd.DataFrame([{
            "NF": numero_nf,
            "Origem": origem,
            "Destino": destino,
            "Valor Produto": vProd,
            "Frete": vFrete,
            "Seguro": vSeg,
            "Base Cálculo": base_calculo,
            "Alíquota": aliquota,
            "ICMS": icms
        }])

    except Exception as e:
        return {"Erro": f"Erro ao processar XML: {e}"}

# _____________________________________________________________________________________________________________ #

import requests

def download_xml_from_access_key(access_key):
    try:
        # Exemplo de URL para baixar o XML
        url = f"https://nfe.fazenda.gov.br/portal/services/xml/{access_key}"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Salvar o XML em um arquivo temporário
            with open("nota_fiscal.xml", "wb") as f:
                f.write(response.content)
            return "nota_fiscal.xml"
        else:
            return None
    except Exception as e:
        print(f"Erro ao baixar XML: {e}")
        return None
