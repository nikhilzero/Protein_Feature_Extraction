import matplotlib.pyplot as plt

# Models and their 10-Fold CV accuracies
models = [
    'SVM', 
    'K-NN', 
    'Naive Bayes', 
    'Random Forest', 
    'Bagging', 
    'ANN (MLP)'
]

accuracies = [
    67.11,  # SVM
    68.25,  # K-NN
    60.63,  # Naive Bayes
    73.05,  # Random Forest
    71.14,  # Bagging Classifier
    72.26   # ANN
]

# Plotting
plt.figure(figsize=(10, 6))
bars = plt.bar(models, accuracies, color='mediumseagreen')
plt.ylim(55, 78)
plt.ylabel('Accuracy (%)')
plt.title('Model Comparison - 10-Fold Cross-Validation Accuracy')

# Add accuracy labels
for bar, acc in zip(bars, accuracies):
    plt.text(bar.get_x() + bar.get_width() / 2, acc + 0.5,
             f'{acc:.2f}%', ha='center', va='bottom', fontsize=9)

plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
