import os 
import glob
import pandas as pd
import numpy as np
import ast
import utils
import preprocessing as pros

# todo 1: unir os vetores das colunas 'channelsNeigh0' e 'channelsNeigh0' OK
# todo 2: retirar o vetor concatenado do vetor de falatantes
    # se for for vazio interpola tudo 
    # se não for vazio interpola os eletrodos que não fazem parte do vetor (substrair )
# todo 3: salvar a nova  
# todo 4: rodar novamente o código de pré-processamento 


def interpol(df, vectorResult, dfNeighbors, file):   
    
    for channel in vectorResult:
        neighbors = dfNeighbors[channel]
        neighbors = neighbors.dropna()
        
        for neigh in neighbors:
            if neigh in vectorResult:
                loc = neighbors.index[neighbors == neigh ][0]
                neighbors[loc] = np.nan
                
        neighbors = neighbors.dropna()
        
        for index in df.index:
            meanNeighbors = df[neighbors].mean(axis=1)
            #df.loc[index, channel] = meanNeighbors
            print(f'values: \n{df[neighbors]}\n')
            print(f'a média é: {meanNeighbors}\n')
            #save_file(file, df)
            
def save_file(file, df):
    name_file = os.path.basename(file)
    df.to_csv(utils.PATH_ARQ_NEW + "/" + name_file)     

def concate_neigh(df, dfNeighbors, file):
    dfAnalysis = pd.read_csv(utils.PATH_ANALYSIS, sep = ",", nrows = 3)

    for indice, file in dfAnalysis.iterrows():
        print(f'file: {file["nameFile"]}')
        vectorConcate =  ast.literal_eval(file["channelsNeigh0"]) + ast.literal_eval(file["channelsNeigh1"])
        vectorMiss = ast.literal_eval(file['channelsMiss'])
        vectorResult = [elemento for elemento in vectorMiss if elemento not in vectorConcate]
        
        #print(f'vetor de faltantes:{vectorMiss}\n')
        #print(f'vetor concatenado: {vectorConcate}\n')
        #print(f'vetor resultante: {vectorResult}\n')
        
        interpol(df, vectorResult, dfNeighbors, file)
        
    

def read_folder():

    csv_folder = glob.glob(os.path.join(utils.PATH_ARQ , "*.csv"))
    dfNeighbors = pros.create_df_Neighbor(utils.PATH_CORRELATION )
  
    for file in csv_folder:
        fileName = os.path.basename(file)
        print(fileName)
        if fileName in utils.ARQ_SEP:
            df = pd.read_csv(file, sep = ",", nrows = 3)
            missElectro = pros.insert_column(df, dfNeighbors)
            concate_neigh(df, dfNeighbors, file)
            
        else:
            df = pd.read_csv(file, sep = "\t", nrows = 3)
            missElectro  = pros.insert_column(df, dfNeighbors)
            concate_neigh(df, dfNeighbors, file)


    

if __name__ == "__main__":
    read_folder()