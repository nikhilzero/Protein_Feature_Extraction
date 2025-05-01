import pandas as pd
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# Step 1: Load the final merged dataset (relative path)
data = pd.read_csv('features/final_training_data.csv')

# Step 2: Separate features and labels
X = data.drop(columns=['Protein_ID', 'Fold'])  # Features
y = data['Fold']                               # Labels

# Step 3: Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Define the SVM model with paper's parameters
svm_model = SVC(kernel='rbf', C=3000, gamma=0.005)

# Step 5: Set up Leave-One-Out Cross-Validation
loo = LeaveOneOut()

# Step 6: Perform LOOCV
scores = cross_val_score(svm_model, X_scaled, y, cv=loo, scoring='accuracy')

# Step 7: Print Results
print("\n✅ Jackknife (LOOCV) Test Results:")
print(f"Mean Jackknife Accuracy: {scores.mean():.2%}")
print(f"Total Proteins: {len(scores)}")
