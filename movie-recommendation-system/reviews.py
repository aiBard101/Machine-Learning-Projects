import bs4 as bs
import urllib.request
import numpy as np
import pickle

class Reviews():
    def __init__(self):
        filename = 'models/nlp_model.pkl'
        self.clf = pickle.load(open(filename, 'rb'))
        self.vectorizer = pickle.load(open('models/tranform.pkl','rb'))

    def get_reviews(self, imdb_id):
        sauce = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
        soup = bs.BeautifulSoup(sauce,'lxml')
        soup_result = soup.find_all("div",{"class":"text show-more__control"})

        reviews_list = [] # list of reviews
        reviews_status = [] # list of comments (good or bad)
        for reviews in soup_result:
            if reviews.string:
                reviews_list.append(reviews.string)
                # passing the review to our model
                movie_review_list = np.array([reviews.string])
                movie_vector = self.vectorizer.transform(movie_review_list)
                pred = self.clf.predict(movie_vector)
                reviews_status.append('Good' if pred else 'Bad')
        if len(reviews_list) > 5:
            return reviews_list[:5], reviews_status[:5]
        return reviews_list, reviews_status
    
if __name__ == "__main__":
    reviews = Reviews()
    imdb_id = "tt1098327"
    print(reviews.get_reviews(imdb_id))