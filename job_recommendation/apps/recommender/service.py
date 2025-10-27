import os
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'data', 'tfidf_vectorizer.joblib')
JOB_MATRIX_PATH = os.path.join(settings.BASE_DIR, 'data', 'job_tfidf_matrix.joblib')
JOB_IDS_PATH = os.path.join(settings.BASE_DIR, 'data', 'job_ids.joblib')


class TFIDFRecommender:
    def __init__(self):
        self.vectorizer = None
        self.job_matrix = None
        self.job_ids = None
        self._load()


    def _load(self):
        try:
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            self.job_matrix = joblib.load(JOB_MATRIX_PATH)
            self.job_ids = joblib.load(JOB_IDS_PATH)
        except Exception:
            self.vectorizer = None
            self.job_matrix = None
            self.job_ids = None


    def is_ready(self):
        return self.vectorizer is not None and self.job_matrix is not None


    def index_jobs(self, job_queryset):
    # Build TF-IDF on job descriptions
        job_texts = [f"{j.title} {j.description} {j.required_skills}" for j in job_queryset]
        if not job_texts:
            raise ValueError("No jobs to index")
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=50000)
        self.job_matrix = self.vectorizer.fit_transform(job_texts)
        self.job_ids = [j.id for j in job_queryset]
        os.makedirs(os.path.dirname(VECTORIZER_PATH), exist_ok=True)
        joblib.dump(self.vectorizer, VECTORIZER_PATH)
        joblib.dump(self.job_matrix, JOB_MATRIX_PATH)
        joblib.dump(self.job_ids, JOB_IDS_PATH)


    def recommend(self, cv_text, top_n=10):
        if not self.is_ready():
            raise RuntimeError('Recommender not indexed')
        cv_vec = self.vectorizer.transform([cv_text])
        sims = cosine_similarity(cv_vec, self.job_matrix).flatten()
        if len(sims) == 0:
            return []
        top_idx = np.argsort(sims)[::-1][:top_n]
        results = []
        for idx in top_idx:
            job_id = self.job_ids[idx]
            score = float(sims[idx])
            results.append({'job_id': job_id, 'score': score})
        return results


    # convenience singleton
    _recommender = None


    def get_recommender():
        global _recommender
        if _recommender is None:
            _recommender = TFIDFRecommender()
        return _recommender