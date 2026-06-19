class RecommendationEngine:
    def __init__(self, df, similarity_matrix):
        self.df = df
        self.similarity_matrix = similarity_matrix
    
    def recommend(self, seed_idx, lambda_param, top_n):
        selected = []
        candidates = [i for i in range(len(self.df)) if i != seed_idx]
        
        while len(selected) < top_n:
            scores = {}
            for candidate in candidates:
                relevance = self.similarity_matrix[seed_idx, candidate]
                if len(selected) == 0:
                    redundancy = 0
                else:
                    redundancy = max([self.similarity_matrix[candidate, s] for s in selected])
                
                mmr_score = lambda_param * relevance - (1 - lambda_param) * redundancy
                scores[candidate] = mmr_score
            
            max_score_candidate = max(scores, key=scores.get)
            selected.append(max_score_candidate)
            candidates.remove(max_score_candidate)
        
        return selected
    
    def get_titles(self, indices):
        return [self.df.iloc[idx]['title'] for idx in indices]