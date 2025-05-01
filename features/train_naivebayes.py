import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB

# Step 1: Load the dataset
data = pd.read_csv('final_training_data.csv')

# Step 2: Separate features and labels
X = data.drop(columns=['Protein_ID', 'Fold'])
y = data['Fold']

# Step 3: Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Define the Naive Bayes model
model = GaussianNB()

# Step 5: Setup 10-Fold Cross-Validation
kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Step 6: Perform Cross-Validation
scores = cross_val_score(model, X_scaled, y, cv=kf, scoring='accuracy')

# Step 7: Output Results
print("\n✅ 10-Fold Cross-Validation for Naive Bayes:")
print(f"Mean Accuracy: {scores.mean():.2%}")
print(f"Standard Deviation: {scores.std():.2%}")
