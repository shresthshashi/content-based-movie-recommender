import pandas as pd

check=0
def code(category,tit,k):
    
    if category==1:
        metadata = pd.read_csv('movies_metadata.csv', low_memory=False)
        if tit not in metadata.values:
            return "key not found"
    elif category==2:
        metadata = pd.read_csv('games_metadata.csv', low_memory=False)
        if tit not in metadata.values:
            return "key not found"
    elif category==3:
        metadata = pd.read_csv('series_metadata.csv', low_memory=False)
        if tit not in metadata.values:
            return "key not found"
    else:
        return "no matched category"
    
   
    metadata.head(3)
    C = metadata['vote_average'].mean()
   # print(C)
    m = metadata['vote_count'].quantile(0.90)
    #print(m)
    q_movies = metadata.copy().loc[metadata['vote_count'] >= m]
    q_movies.shape
    def weighted_rating(x, m=m, C=C):
        v = x['vote_count']
        R = x['vote_average']
        # Calculation based on the IMDB formula
        return (v/(v+m) * R) + (m/(m+v) * C)
    q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
    q_movies = q_movies.sort_values('score', ascending=False)

    from sklearn.feature_extraction.text import TfidfVectorizer

    #Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words='english')

    #Replace NaN with an empty string
    metadata['overview'] = metadata['overview'].fillna('')

    #Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(metadata['overview'])

    #Output the shape of tfidf_matrix
    #print(tfidf_matrix.shape)

    from sklearn.metrics.pairwise import linear_kernel

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(metadata.index, index=metadata['title']).drop_duplicates()
    
    def get_recommendations(title, cosine_sim=cosine_sim):
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1:k+1]
        movie_indices = [i[0] for i in sim_scores]
        result=metadata['title'].iloc[movie_indices]
        return result
    x=get_recommendations(tit)
    x=x.tolist()
    return x


























