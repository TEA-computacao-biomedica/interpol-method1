import os 
import glob
import numpy as np
import pandas as pd
import utils as utils

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

def insert_column(df, dfNeighbors):
  
  missElectrode = []
  
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
  
  return missElectrode

# Função que checa se existe algum eletrodo com menos de dois vizinhos

def remove_nan_neighbors(df, missElectrode, dfNeighbors):
 
  neigh0 = []
  neigh1 = []
  
  for electrode in missElectrode:
    neighbors = dfNeighbors[electrode]
    neighbors = neighbors.dropna()
    
    for neigh in neighbors:
      if neigh in missElectrode:
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

def save_file(path, nameFile, df):
    df.to_csv(''.join(path) + "/" + nameFile, index= False)  
  
  
def read_folder():
  
  csv_folder = glob.glob(os.path.join(utils.PATH_FILES , "*.csv"))
  dfNeighbors = create_df_Neighbor(utils.PATH_CORRELATION )
  
  for file in csv_folder:
    fileName = os.path.basename(file)
    nameFile.append(fileName)
    
    if fileName in utils.ARQ_SEP:
        df = pd.read_csv(file, sep = ",", nrows = 3)
        missElectro = insert_column(df, dfNeighbors)
        remove_nan_neighbors(df, missElectro , dfNeighbors)
        
    else:
        df = pd.read_csv(file, sep = "\t", nrows = 3)
        missElectro  = insert_column(df, dfNeighbors)
        remove_nan_neighbors(df, missElectro, dfNeighbors)



if __name__ == "__main__":
  read_folder()
  analysis['nameFile'] = nameFile
  analysis['channelsMiss'] = channelsMiss
  analysis['qtdMiss'] = qtdMiss

  analysis['channelsNeigh0'] = channelsNeigh0
  analysis['channelsNeigh1'] = channelsNeigh1

  analysis['qtdNeigh1'] = qtdNeigh1
  analysis['qtdNeigh0'] = qtdNeigh0
  
  save_file( './','analysis_missing.csv', analysis)

  
