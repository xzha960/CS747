import pandas as pd
import numpy as np

# 创建数据表
data = {
    "Error Type": [
        "grammarly-errors", "logic-errors", "function-design-errors",
        "conditional-judgment-errors", "loop-termination-condition",
        "uninitialized-variable-errors", "type-errors", "calculation-errors",
        "list-indexing-errors", "input-output-format-errors"
    ],
    "Accuracy (E1)": [92.04, 81.26, 80.33, 79.63, 81.26, 80.80, 80.09, 81.03, 80.33, 79.63],
    "Avg. Score (E1)": [95.30, 88.63, 90.07, 91.32, 89.82, 90.81, 90.08, 90.41, 90.34, 90.54],
    "Accuracy (E2)": [82.44, 82.90, 79.63, 80.09, 81.26, 79.63, 81.03, 81.26, 80.09, 80.56],
    "Avg. Score (E2)": [80.67, 80.37, 87.40, 87.34, 87.58, 87.54, 86.66, 87.67, 86.79, 86.51]
}

df = pd.DataFrame(data)

# 计算准确率与平均分数的方差
variance_results = {
    "Accuracy (E1) Variance": np.var(df["Accuracy (E1)"], ddof=0),
    "Accuracy (E2) Variance": np.var(df["Accuracy (E2)"], ddof=0),
    "Avg. Score (E1) Variance": np.var(df["Avg. Score (E1)"], ddof=0),
    "Avg. Score (E2) Variance": np.var(df["Avg. Score (E2)"], ddof=0)
}

print(variance_results)
