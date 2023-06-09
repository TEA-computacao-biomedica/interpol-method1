import os 
import glob
import pandas as pd
import numpy as np
import ast
import utils as utils
import preprocessing as pros

def first_interpol(df, vectorResult, vectorMiss, dfNeighbors, nameFile, path):  
    
    for channel in vectorResult:
        neighbors = dfNeighbors[channel]
        neighbors = neighbors.dropna()
    
        for neigh in neighbors:
            if neigh in vectorMiss:
                loc = neighbors.index[neighbors == neigh ][0]
                neighbors[loc] = np.nan
                neighbors = neighbors.dropna()
        
        for index, row in df.iterrows():
            meanNeighbors = row[neighbors].mean()
            df.loc[index, channel] = round(meanNeighbors,4)
            
    pros.save_file(path, nameFile, df)
       
def second_interpol():
    csv_folder = glob.glob(os.path.join(utils.PATH_FILES_INTERPOLATED, "*.csv")) 
    dfSecondInterpol = pd.read_csv(utils.PATH_ANALYSIS_SECOND_INTERPOLATED, sep = ",")
    dfNeighbors = pros.create_df_Neighbor(utils.PATH_CORRELATION )
    
    for file in csv_folder:
        fileName = os.path.basename(file)
        if fileName in utils.FILES_SECOND_INTERPOLATED:
            df = pd.read_csv(file, sep = ",")
            vectorResult = ast.literal_eval(dfSecondInterpol.loc[dfSecondInterpol['FileName'] == fileName, 'FinalList4Interpol'].item())
            vectorMiss = ast.literal_eval(dfSecondInterpol.loc[dfSecondInterpol['FileName'] == fileName, 'MissingChannels'].item())
            first_interpol(df, vectorResult, vectorMiss, dfNeighbors, fileName, utils.PATH_FILES_SECOND_INTERPOLATED)
        




def concate_neigh(df, dfNeighbors, fileName):
    dfAnalysis = pd.read_csv(utils.PATH_ANALYSIS, sep = ",")
    
    for index, row in dfAnalysis.iterrows():
        if row['nameFile'] == fileName:
            vectorMiss = ast.literal_eval(row['channelsMiss'])
            vectorConcate =  ast.literal_eval(row["channelsNeigh0"]) + ast.literal_eval(row["channelsNeigh1"])
            vectorResult = [elemento for elemento in vectorMiss if elemento not in vectorConcate]
    
    first_interpol(df, vectorResult, vectorMiss, dfNeighbors, fileName, utils.PATH_FILES_SECOND_INTERPOLATED)     

    
        
def read_folder(path):

    csv_folder = glob.glob(os.path.join(path, "*.csv"))
    dfNeighbors = pros.create_df_Neighbor(utils.PATH_CORRELATION )
  
    for file in csv_folder:
        fileName = os.path.basename(file)
        if fileName in utils.ARQ_SEP:
            df = pd.read_csv(file, sep = ",")
            if 'UNNAMED: 0' in df.columns:
                df = df.drop('UNNAMED: 0', axis=1) 
            missElectro = pros.insert_column(df, dfNeighbors)
            concate_neigh(df, dfNeighbors, fileName)
            
        else:
            df = pd.read_csv(file, sep = "\t")
            if 'UNNAMED: 0' in df.columns:
                df = df.drop('UNNAMED: 0', axis=1) 
            missElectro  = pros.insert_column(df, dfNeighbors)
            concate_neigh(df, dfNeighbors, fileName)

if __name__ == "__main__":
    #read_folder(utils.PATH_FILES)
    second_interpol()