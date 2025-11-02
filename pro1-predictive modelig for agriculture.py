# All required libraries are imported here for you.
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
# Load the dataset
crops = pd.read_csv("soil_measures.csv")
print(crops.columns)
# Write your code here
X = crops[["N", "P", "K", "ph"]]
y = crops["crop"]

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 存放每个特征的评估结果
scores = {}

# 按特征单独训练模型，评估预测能力
for i, feature in enumerate(X.columns):
    model = LogisticRegression(max_iter=500, multi_class="multinomial")
    # 只用单个特征
    model.fit(X_train_scaled[:, i].reshape(-1, 1), y_train)
    y_pred = model.predict(X_test_scaled[:, i].reshape(-1, 1))
    acc = accuracy_score(y_test, y_pred)  # 这里用准确率作为评价指标
    scores[feature] = acc

# 找到最好特征
best_feature = max(scores, key=scores.get)

# 构建字典
best_predictive_feature = {best_feature: scores[best_feature]}

print(best_predictive_feature)





