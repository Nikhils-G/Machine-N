# Re-import necessary packages after kernel reset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB

# Sample data simulating scraped business information
data = pd.DataFrame({
    'HasWebsite': [1, 0, 1, 1, 0, 0, 1, 1],
    'KeywordMatch': [1, 1, 0, 1, 0, 0, 1, 1],
    'CityTier': [1, 2, 3, 1, 3, 2, 1, 1],
    'EmailAvailable': [1, 0, 0, 1, 0, 0, 1, 1],  # Target for model 1
    'LeadScore': [9, 3, 4, 10, 2, 3, 9, 8],      # Target for model 2 (regression or classification bin)
    'BusinessDesc': [
        "Interior design and architectural consultation",
        "Local grocery and food supplies",
        "Online education startup for tech skills",
        "Digital marketing and branding agency",
        "Street food and small restaurant",
        "Handmade clothing store",
        "Corporate law consultancy",
        "Health and fitness center"
    ],
    'BusinessCategory': [
        "Design", "Retail", "EdTech", "Marketing",
        "Food", "Retail", "Legal", "Health"
    ]  # Target for model 3
})

# Separate datasets for each model purpose
X1 = data[['HasWebsite', 'KeywordMatch', 'CityTier']]
y1 = data['EmailAvailable']

X2 = data[['HasWebsite', 'KeywordMatch', 'CityTier']]
y2 = (data['LeadScore'] > 6).astype(int)  # High-value leads

X3_text = data['BusinessDesc']
y3 = data['BusinessCategory']

# Model 1: Email Prediction
model_email = RandomForestClassifier(random_state=42)
model_email.fit(X1, y1)

# Model 2: Lead Scoring
model_score = GradientBoostingClassifier(random_state=42)
model_score.fit(X2, y2)

# Model 3: Business Category Classifier (NLP)
pipeline_nlp = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=50)),
    ('clf', MultinomialNB())
])
pipeline_nlp.fit(X3_text, y3)

# Testing sample prediction
test_sample = pd.DataFrame({
    'HasWebsite': [1],
    'KeywordMatch': [1],
    'CityTier': [1]
})

email_pred = model_email.predict(test_sample)
score_pred = model_score.predict(test_sample)
category_pred = pipeline_nlp.predict(["Experienced digital growth agency for startups"])

(email_pred[0], score_pred[0], category_pred[0])
