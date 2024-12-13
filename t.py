import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

# Load the dataset
df = pd.read_csv("a.csv")

# Feature selection
X = df[['SquareFootage', 'Location', 'PreConstruction', 'Construction', 'PostConstruction']]
y = df['TotalCost']

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessing: One-hot encoding for categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), ['Location']),
    ],
    remainder='passthrough'  # Keep the other columns as they are
)

# Create a pipeline with preprocessing and the model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor(objective='reg:squarederror'))
])

# Hyperparameter tuning using Grid Search
param_grid = {
    'regressor__n_estimators': [100, 200],
    'regressor__max_depth': [3, 5, 7],
    'regressor__learning_rate': [0.01, 0.1, 0.2]
}

grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error', verbose=1)
grid_search.fit(X_train, y_train)

# Best model from grid search
best_model = grid_search.best_estimator_

# Save the trained model
joblib.dump(best_model, "optimized_house_price_model_xgb.pkl")

# Evaluate the best model
predictions = best_model.predict(X_test)

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(y_test, predictions))
print("Predictions:", predictions)
print("Actual:", y_test.values)
print("RMSE:", rmse)