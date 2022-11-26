# Bibliotecas
# pip install geopandas
# pip install shapely
import geopandas as gdf
import shapely as shpy
import fiona
import os

def limparArquivos(pasta):
    arquivos = os.listdir(pasta)
    for arquivos_individual in arquivos:
        os.remove(os.path.join(pasta,arquivos_individual))
        

def padronizacao(vetor, pasta):
    shpy.ops.polygonize(vetor)
    vetor = vetor.explode(index_parts=True)
    projecao = vetor.crs
    if projecao != 'epsg:4326':
        vetor = vetor.to_crs("EPSG:4326")
    vetor.to_file(r'{}\lines.shp.zip'.format(pasta), driver='ESRI Shapefile') 


def extensao(pasta):
    arquivosPasta = os.listdir(pasta)
    extensoes = ['shp', 'geojson', 'kml']
    for arquivo_individual in arquivosPasta:
        separacao = arquivo_individual.split('.')
        extensao_arquivo = separacao[-1]
        if extensao_arquivo in extensoes:
            extensao_caminho = {'extensao':extensao_arquivo, 'caminho':r'{}\{}'.format(pasta,arquivo_individual)}  
            return extensao_caminho


def entrada_arquivo(pasta):
    caminho_arquivo = extensao(pasta)
    if caminho_arquivo['extensao'] == 'kml':
        fiona.drvsupport.supported_drivers['KML'] = 'rw'
        vetor = gdf.read_file(caminho_arquivo['caminho'], driver='kml')
    else:
        vetor = gdf.read_file(caminho_arquivo['caminho'], driver=caminho_arquivo['extensao'])
    padronizacao(vetor, pasta)
