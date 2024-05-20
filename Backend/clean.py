import pandas as pd 
import json 
df=pd.read_csv('anime.csv')
df=df.drop(columns=['episodes','members','type'])
genre=df['genre']
Unique_genre=[]
for x in genre:
    if type(x)==str:
        x = "".join(x.split())
        y= x.split(',')  
    else:
        df=df.drop(df[df['genre']==x].index)
    Unique_genre+=y
    
Unique_genre=list(set(Unique_genre))
df=df.dropna(how='any')

data={}

data['genre']=Unique_genre
data['data']=df.to_dict('records')
data['users']=[]
with open('anime.json', 'w') as file:
    json.dump(data, file, indent=4)

