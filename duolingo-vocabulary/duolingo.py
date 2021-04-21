import pandas as pd
import numpy as np

def write_csv(df, doc_name):
    df = df.drop(columns=['Categoria gramatical'])
    doc = open(doc_name, 'w')
    doc.write(df.to_csv(header=False, index=False))
    doc.close()

csv = input('CSV file address: ')

df = pd.read_csv (csv)
df = df.drop(columns=['Grau de confiança', 'Última prática'])
df = df.dropna()

for categoria in ['Verb', 'Noun', 'Adjective', 'Adverb']:
    write_csv(df.loc[df['Categoria gramatical'] == categoria], categoria.lower() + '.csv')