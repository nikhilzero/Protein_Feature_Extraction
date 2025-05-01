import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

# Step 1: Load the dataset
data = pd.read_csv('final_training_data.csv')

# Step 2: Separate features and target
X = data.drop(columns=['Protein_ID', 'Fold'])
y = data['Fold']

# Step 3: Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Define the Bagging model (base estimator = Decision Tree)
base_estimator = DecisionTreeClassifier()
model = BaggingClassifier(estimator=base_estimator, n_estimators=100, random_state=42)


# Step 5: Setup 10-Fold Stratified Cross-Validation
kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Step 6: Perform Cross-Validation
scores = cross_val_score(model, X_scaled, y, cv=kf, scoring='accuracy')

# Step 7: Output Results
print("\n✅ 10-Fold Cross-Validation for Bagging Classifier:")
print(f"Mean Accuracy: {scores.mean():.2%}")
print(f"Standard Deviation: {scores.std():.2%}")
