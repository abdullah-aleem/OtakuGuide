class Recommendation:
    def __init__(self):
        self.model = None
        self.data = None
        
    def addWatched(self, user_id, anime_id,rating):
        self.data['users'][user_id]['watched'].append({'rating': rating, 'anime_id': anime_id})
    
    def addUser(self, name):
        self.data['users'].append({'id': 0, 'watched': [],'name':name,'favGenre':[],'uniqueQuotient':0,'similarUsers':[]})
    
    def recommend(self, user_id):
        #whole recommending procedure would in this funciton including collaborative and content based filtering 
        pass
        
    def load_data(self, data):
        self.data = data

    def load_model(self, model):
        self.model = model

    def recommend(self, user_id):
        return self.model.predict(user_id, self.data)