import fitz # PyMuPDF
import re
from celery import shared_task
from apps.cvs.models import CV
from apps.recommender.service import get_recommender


@shared_task
def process_cv(cv_id):
    cv = CV.objects.get(id=cv_id)
    # 1. extract text
    doc = fitz.open(stream=cv.file.read(), filetype='pdf')
    text_chunks = [page.get_text() for page in doc]
    raw_text = "\n".join(text_chunks)
    # 2. simple clean
    text = raw_text.replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    # 3. naive skill extraction (regex + keywords)
    # For production, use spaCy NER or dedicated skill list
    skills = []
    skill_candidates = ['python','django','react','sql','excel','powerbi','rest','api']
    lower = text.lower()
    for s in skill_candidates:
        if s in lower:
            skills.append(s)
    # 4. persist
    cv.extracted_text = text
    cv.parsed_skills = skills
    cv.processed = True
    cv.save()


    # 5. optionally compute recommendations synchronously
    rec = get_recommender()
    if rec.is_ready():
        _ = rec.recommend(text, top_n=10) # caller can query via view
    return True