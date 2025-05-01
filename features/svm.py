import pandas as pd
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# Step 1: Load the final merged dataset
data = pd.read_csv('final_training_data.csv')

# Step 2: Separate features and labels
X = data.drop(columns=['Protein_ID', 'Fold'])  # Features
y = data['Fold']                               # Target labels

# Step 3: Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Create SVM model
svm_model = SVC(kernel='rbf', C=3000, gamma=0.005)

# Step 5: Set up 10-Fold Stratified Cross Validation
kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Step 6: Perform cross-validation
scores = cross_val_score(svm_model, X_scaled, y, cv=kf, scoring='accuracy')

# Step 7: Print Results
print("\n✅ 10-Fold Cross-Validation Scores (per fold):")
print(scores)
print(f"\n✅ Mean Cross-Validation Accuracy: {scores.mean():.2%}")
print(f"✅ Standard Deviation: {scores.std():.2%}")
