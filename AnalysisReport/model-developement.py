import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv("/mnt/data/leads_dataset.csv")

data['Has_Email'] = data['Email'].apply(lambda x: 0 if x == 'Not found' else 1)
data['Business_Length'] = data['Business Name'].apply(lambda x: len(x))
data['Website_Present'] = data['Maps URL'].apply(lambda x: 0 if not isinstance(x, str) or x == '' else 1)

features = data[['Has_Email', 'Business_Length', 'Website_Present']]
target = data['Quality_Label']

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

model_path = "/mnt/data/lead_quality_model.pkl"
joblib.dump(model, model_path)

accuracy, model_path
