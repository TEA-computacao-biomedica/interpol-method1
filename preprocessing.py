import os 
import glob
import numpy as np
import pandas as pd
import utils

analysis = pd.DataFrame(columns=['nameFile', 'channelsMiss', 'qtdMiss', 'channelsNeigh0',  'qtdNeigh0', 'channelsNeigh1',  'qtdNeigh1' ])

nameFile = []
channelsMiss = []
qtdMiss = []
channelsNeigh0 =[]
qtdNeigh0 = []
channelsNeigh1 = []
qtdNeigh1 = []

# Função que ler o csv com os vizinhos de cada eletrodo e retorna um dataframe
 
def create_df_Neighbor(path):

  df = pd.read_csv(path, sep= ",", skiprows= 4)

  df.columns = df.columns.str.upper()
  df = df.apply(lambda x: x.str.upper() if x.dtype == 'object' else x)
  
  return df

# Função que encontra a posição do eletrodo faltante e insere uma coluna com nan ou 0 

def insert_column(file, sep, dfNeighbors):

  missElectrode = []

  df = pd.read_csv(file, sep = sep, nrows = 3)

  df.columns = df.columns.str.upper()
  
  for col in utils.CHANNELS:
    if col not in df.columns:
      if col == 'CZ':
        loc = utils.CHANNELS.index(col)
        df.insert(loc, col, 0)
      else:
        missElectrode.append(col)
        loc = utils.CHANNELS.index(col)
        df.insert(loc, col, np.nan)
        
  lenMiss = len(missElectrode)
  qtdMiss.append(lenMiss)
  channelsMiss.append(missElectrode) 

  mean_neighbors(df, missElectrode, dfNeighbors)

# Função que checa se existe algum eletrodo com menos de dois vizinhos

def mean_neighbors(df, missElectrode, dfNeighbors):
 
  neigh0 = []
  neigh1 = []

  for electrode in missElectrode:
    neighbors = dfNeighbors[electrode]
    neighbors = neighbors.dropna()

    for neigh in neighbors:
      if df[neigh].isna().any():
        loc = neighbors.index[neighbors == neigh ][0]
        neighbors[loc] = np.nan
        
    neighbors = neighbors.dropna()

    if len(neighbors) == 0:
      neigh0.append(electrode)
      
    if len(neighbors) == 1:
      neigh1.append(electrode)

  lenNeigh0 =  len(neigh0)
  lenNeigh1 =  len(neigh1)

  channelsNeigh0.append(neigh0)
  channelsNeigh1.append(neigh1)
  qtdNeigh1.append(lenNeigh1)
  qtdNeigh0.append(lenNeigh0)
  

if __name__ == "__main__":
    csv_folder = glob.glob(os.path.join(utils.PATH_ARQ , "*.csv"))

    dfNeighbors = create_df_Neighbor(utils.PATH_CORRELATION )

    for file in csv_folder:
        nameFolder = os.path.basename(file)
        nameFile.append(nameFolder)
        print("\n" + nameFolder)
        if nameFolder in utils.ARQ_SEP:
            insert_column(file, ",", dfNeighbors)
        else:
            insert_column(file, "\t", dfNeighbors)

    analysis['nameFile'] = nameFile
    analysis['channelsMiss'] = channelsMiss
    analysis['qtdMiss'] = qtdMiss

    analysis['channelsNeigh0'] = channelsNeigh0
    analysis['channelsNeigh1'] = channelsNeigh1

    analysis['qtdNeigh1'] = qtdNeigh1
    analysis['qtdNeigh0'] = qtdNeigh0

    analysis.to_csv('analise_faltantes.csv', index=False)
  
