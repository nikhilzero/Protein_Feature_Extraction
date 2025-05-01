import pandas as pd
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('final_training_data.csv')
X = data.drop(columns=['Protein_ID', 'Fold'])
y = data['Fold']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = BaggingClassifier(estimator=DecisionTreeClassifier(), n_estimators=100, random_state=42)
loo = LeaveOneOut()

scores = cross_val_score(model, X_scaled, y, cv=loo, scoring='accuracy')

print("\n✅ Jackknife (LOOCV) Test Results for Bagging Classifier:")
print(f"Mean Jackknife Accuracy: {scores.mean():.2%}")
print(f"Total Proteins: {len(scores)}")
