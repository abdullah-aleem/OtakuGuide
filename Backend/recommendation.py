import json
from collections import Counter
import math 

class Recommendation:
    def __init__(self):
        with open('anime.json') as file:
            self.data = json.load(file)
        if len(self.data['users'])==0:
            self.count=0
        else:
            self.count=self.data['users'][-1]['id']
        
    def addWatched(self, user_id, anime_id,rating):
        watched={'rating': rating, 'anime_id': anime_id}
        if not watched in self.data['users'][user_id-1]['watched']:
            self.data['users'][user_id-1]['watched'].append(watched)
            self.save_data()
            self.favoriteGenre(user_id)
            self.similarUser(user_id)
            self.save_data()
        return
    
    def addUser(self, name):
        self.count+=1
        user={'id': self.count, 'watched': [],'name':name,'favGenre':[],'uniqueQuotient':0,'similarUsers':[]}
        self.data['users'].append(user)
        self.save_data()
        return user
    
    
    
    def recommend(self, user_id):
        if self.data['users'][user_id-1]['watched']==[]:
            return sorted(self.data['data'],key=lambda x:x['rating'],reverse=True)[:15]
        #contetnt based filtering
        resultcontent=[]
        resultcollaborative=[]
        contentAnime=[]
        for anime in self.data['data']:
            
            list1=set("".join(anime['genre'].split()).split(','))
            list2=set(self.data['users'][user_id-1]['favGenre'])
            common=list1.intersection(list2)
            if len(common)>0:
                contentAnime.append({"id":anime['anime_id'],'common':len(common)})
            
        contentAnime=sorted(contentAnime,key=lambda x:x['common'],reverse=True)
        contentAnime=contentAnime[:6]
        
        for x in contentAnime:
            resultcontent.append(self.data['data'][x['id']])
        
        #collaborative filtering
        for x in self.data['users'][user_id-1]['similarUsers']:
            count=0
            for y in self.data['users'][x['user']-1]['watched']:
                if not y in self.data['users'][user_id-1]['watched']:
                    resultcollaborative.append(self.data['data'][y['anime_id']])
                    count+=1
                if count==2:
                    break
        len_array1 = int(len(resultcollaborative) * (1 - self.data['users'][user_id-1]['uniqueQuotient']))
        len_array2 = int(len(resultcontent) * self.data['users'][user_id-1]['uniqueQuotient'])
    
        interpolated_array = resultcollaborative[:len_array1] + resultcontent[:len_array2]
    
            
        return interpolated_array        
        
        
        
        
    
    def favoriteGenre(self,user_id):
        animelist=self.data['users'][user_id-1]['watched']
        genres=[]
        for anime in animelist:
            genres+="".join(self.data['data'][anime['anime_id']]['genre'].split()).split(',')
        counter = Counter(genres)
        most_common_items = counter.most_common(3)  
        self.data['users'][user_id-1]['favGenre']=[x[0] for x in most_common_items]

    
    def similarUser(self,user_id):
        users=self.data['users']
        similarity=[]
        
        for x in users:
            list1=[]
            list2=[]
            if x['id']!=user_id:
                for y in users[user_id-1]['watched']:
                    temp=[z['anime_id'] for z in x['watched']]
                    if y['anime_id'] in temp:
                            list1.append(y['rating'])
                            list2.append(x['watched'][temp.index(y['anime_id'])]['rating'])
                
                
                similarity.append({'similarity':self.cosine_similarity(list1,list2),'user':x['id']})
        self.data['users'][user_id-1]['similarUsers']=sorted(similarity,key=lambda x:x['similarity'],reverse=True)[:3]
        uniqueQuotient=1.25-sum([x['similarity'] for x in similarity[:3]])/len([x['similarity'] for x in similarity[:3]])
        self.data['users'][user_id-1]['uniqueQuotient']=uniqueQuotient
        
    
    @staticmethod
    def cosine_similarity(list1, list2):
        print(list1,list2)
        dot_product = sum(a * b for a, b in zip(list1, list2))
        magnitude1 = math.sqrt(sum(a * a for a in list1))
        magnitude2 = math.sqrt(sum(b * b for b in list2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        print(dot_product)
        print(magnitude1*magnitude2)
        return dot_product / (magnitude1 * magnitude2)

    def save_data(self):
        with open('anime.json', 'w') as file:
            json.dump(self.data, file, indent=4)
        return
