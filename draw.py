import matplotlib.pyplot as plt
import pandas as pd

# Data
data = {
    "Error Type": [
        "grammarly-errors", "logic-errors", "function-design-errors",
        "conditional-judgment-errors", "loop-termination-condition",
        "uninitialized-variable-errors", "type-errors",
        "calculation-errors", "list-indexing-errors", "input-output-format-errors"
    ],
    "Accuracy (E1)": [92.04, 81.26, 80.33, 79.63, 81.26, 80.80, 80.09, 81.03, 80.33, 79.63],
    "Accuracy (E2)": [82.44, 82.90, 79.63, 80.09, 81.26, 79.63, 81.03, 81.26, 80.09, 80.56],
    "Avg. Score (E1)": [95.30, 88.63, 90.07, 91.32, 89.82, 90.81, 90.08, 90.41, 90.34, 90.54],
    "Avg. Score (E2)": [80.67, 80.37, 87.40, 87.34, 87.58, 87.54, 86.66, 87.67, 86.79, 86.51]
}

df = pd.DataFrame(data)

# Plot Accuracy
plt.figure(figsize=(10, 6))
x = range(len(df))
bar_width = 0.4

plt.bar(x, df["Accuracy (E1)"], width=bar_width, label="Accuracy (E1:EduFix)")
plt.bar([i + bar_width for i in x], df["Accuracy (E2)"], width=bar_width, label="Accuracy (E2:Baseline)")

plt.xticks([i + bar_width / 2 for i in x], df["Error Type"], rotation=45, ha="right")
plt.ylabel("Accuracy (%)")
plt.title("Figure 4.1 Accuracy Comparison")
plt.legend()
plt.tight_layout()
plt.savefig("accuracy_comparison.png", dpi=300)

# Plot Avg. Score
plt.figure(figsize=(10, 6))

plt.bar(x, df["Avg. Score (E1)"], width=bar_width, label="Avg. Score (E1:EduFix)")
plt.bar([i + bar_width for i in x], df["Avg. Score (E2)"], width=bar_width, label="Avg. Score (E2:Baseline)")

plt.xticks([i + bar_width / 2 for i in x], df["Error Type"], rotation=45, ha="right")
plt.ylabel("Average Score")
plt.title("Figure 4.2 Average Score Comparison")
plt.legend()
plt.tight_layout()
plt.savefig("score_comparison.png", dpi=300)
