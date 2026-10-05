from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from typing import List, Dict, Any

class TopicModeler:
    def __init__(self, n_topics: int = 5, n_top_words: int = 10):
        self.n_topics = n_topics
        self.n_top_words = n_top_words
        self.vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
        self.nmf = NMF(n_components=self.n_topics, random_state=42, init='nndsvda')
        self.feature_names = []
        self.topics = {}
        
    def fit(self, texts: List[str]) -> None:
        """
        Fits the topic model on a corpus of cleaned texts.
        """
        if not texts:
            return
            
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        self.nmf.fit(tfidf_matrix)
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        self.topics = {}
        for topic_idx, topic in enumerate(self.nmf.components_):
            top_features_ind = topic.argsort()[:-self.n_top_words - 1:-1]
            top_features = [self.feature_names[i] for i in top_features_ind]
            self.topics[topic_idx] = " ".join(top_features)

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predicts the dominant topic for a given text.
        """
        if not text or not self.topics:
            return {"topic_id": -1, "topic_label": "Unknown"}
            
        tfidf = self.vectorizer.transform([text])
        topic_distribution = self.nmf.transform(tfidf)[0]
        
        dominant_topic_id = int(topic_distribution.argmax())
        
        return {
            "topic_id": dominant_topic_id,
            "topic_label": self.topics.get(dominant_topic_id, "Unknown")
        }
        
    def get_topics(self) -> Dict[int, str]:
        """
        Returns the discovered topics and their keywords.
        """
        return self.topics

# Singleton instance to be trained when enough data is present
topic_modeler = TopicModeler()
