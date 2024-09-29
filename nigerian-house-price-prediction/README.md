# Nigerian House Price Prediction

This project aims to predict the prices of houses in Nigeria using various machine learning models. The dataset contains detailed information about different properties across Nigeria, including the number of bedrooms, bathrooms, state, town, and house type. The project covers data preprocessing, feature engineering, model development, evaluation, and deployment as a web application.

## Table of Contents

- [Project Overview](#project-overview)
- [Dataset Description](#dataset-description)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Data Preprocessing](#data-preprocessing)
- [Feature Engineering](#feature-engineering)
- [Model Development](#model-development)
- [Evaluation](#evaluation)
- [Hyperparameter Tuning](#hyperparameter-tuning)
- [Running the Web Application](#running-the-web-application)
- [Results](#results)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The goal of this project is to predict house prices in Nigeria based on various features such as the number of bedrooms, bathrooms, state, town, and the type of house. Multiple regression models are developed, and the most optimal model is selected based on performance metrics.

The project utilizes a wide range of machine learning algorithms, including:

- Linear Regression
- Ridge Regression
- Decision Trees
- Random Forest
- Support Vector Regressor (SVR)
- K-Nearest Neighbors (KNN)
- XGBoost Regressor

Hyperparameter tuning is performed using `GridSearchCV` to optimize the Random Forest, XGBoost, and SVR models.

## Dataset Description

The dataset consists of Nigerian house listings, including the following key features:

- **Bedrooms**: Number of bedrooms
- **Bathrooms**: Number of bathrooms
- **Toilets**: Number of toilets
- **State**: State where the house is located
- **Town**: Town where the house is located
- **Title**: Type of house (e.g., Detached Duplex, Terraced Duplex)
- **Price**: The price of the house (target variable)

The dataset includes a variety of numerical and categorical features.

## Requirements

The project requires Python 3.x and the following libraries:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `xgboost`
- `pickle`
- `fastapi`
- `uvicorn`
- `jinja2`
- `pydantic`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/aiBard101/Machine-Learning-Projects.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd Machine-Learning-Projects/nigerian-house-price-prediction
   ```

3. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment:**

   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **On macOS and Linux:**
     ```bash
     source venv/bin/activate
     ```

5. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Download the dataset:**

   - Place your `nigeria_houses_data.csv` file in the `dataset/` folder.

## Project Structure

```
.
├── dataset/
    ├── nigeria_houses_data.csv
│   └── X_data.csv
├── models/
│   ├── linear_reg.pkl
│   ├── ridge_reg.pkl
│   ├── decision_tree.pkl
│   ├── random_forest.pkl
│   ├── xgb_reg.pkl
│   ├── svr_reg.pkl
│   ├── knn_reg.pkl
│   ├── state_town_dict.json
│   └── house_title.json
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
├── main.py
├── motebook.ipynb
├── predict.py
├── README.md
└── requirements.txt
```

- **dataset/**: Contains the dataset used for training and testing.
- **models/**: Contains the trained machine learning models and auxiliary data files (e.g., encoders, dictionaries).
- **static/**: Contains static assets like CSS and JavaScript files.
- **templates/**: Contains HTML templates for web rendering.
- **main.py**: The main FastAPI application file.
- **predict.py**: Contains the prediction logic.
- **README.md**: This README file.
- **requirements.txt**: Lists all Python dependencies.
- **X_data.csv**: Processed feature data used for modeling.

## Data Preprocessing

The following steps were performed to prepare the dataset:

1. **Handling Missing Values**: Identified and handled missing values by either removing or imputing them with appropriate substitutes.

2. **Encoding Categorical Variables**: Categorical features such as `state`, `town`, and `title` were encoded using label encoding and one-hot encoding techniques.

3. **Outlier Detection**: Identified outliers in the `price` feature using statistical methods (e.g., z-score and interquartile range) and handled them appropriately. Applied log transformations to normalize the distribution.

4. **Feature Scaling**: Scaled numerical features using `MinMaxScaler` to normalize the data.

## Feature Engineering

- **Price Transformation**: Applied log transformation to the target variable `price` to reduce skewness.

- **New Feature Creation**: Created a combined `townState` feature by merging the `town` and `state` columns to better represent geographic information.

- **Rank Encoding**: Rank-encoded the house `title` (e.g., Detached Duplex, Terraced Bungalow) to introduce an ordinal relationship.

## Model Development

The following models were developed and evaluated:

1. **Linear Regression**: Established a baseline model to understand linear relationships between features and the target variable.

2. **Ridge and Lasso Regression**: Used regularized regression models to handle multicollinearity and prevent overfitting.

3. **Decision Tree Regressor**: Employed tree-based methods to capture non-linear relationships in the data.

4. **Random Forest Regressor**: Utilized an ensemble of decision trees to improve generalization and reduce variance.

5. **Support Vector Regressor (SVR)**: Tested with different kernels to capture complex relationships between features.

6. **K-Nearest Neighbors (KNN)**: Used a distance-based method to predict based on neighboring data points.

7. **XGBoost Regressor**: Leveraged a powerful gradient boosting method to enhance prediction performance.

## Evaluation

The models were evaluated using the following metrics:

- **Mean Absolute Error (MAE)**: Average absolute difference between predicted and actual values.
- **Mean Squared Error (MSE)**: Average squared difference between predicted and actual values.
- **Root Mean Squared Error (RMSE)**: Square root of the MSE for easier interpretation.
- **R-squared (R²)**: Indicates the proportion of variance in the target variable explained by the features.

By comparing these metrics, Random Forest and XGBoost emerged as the top-performing models for predicting house prices in Nigeria.

## Hyperparameter Tuning

To further improve model performance, `GridSearchCV` was used to fine-tune hyperparameters for models like Random Forest, XGBoost, and SVR. The parameters tested included the number of trees, maximum depth, learning rate, and more. This optimization helped the models achieve better generalization on unseen data.

### Example of GridSearchCV for Random Forest:

```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf = RandomForestRegressor(random_state=42)
rf_grid = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
rf_grid.fit(X_train, y_train)
```

## Running the Web Application

The web application allows users to input house features and receive a predicted price based on the trained machine learning models. The application is built using FastAPI for the backend and HTML/CSS/JavaScript for the frontend.

### Prerequisites

- Ensure all dependencies are installed (see [Installation](#installation)).
- Make sure the trained models and JSON files are present in the `models/` directory.
- Verify that the `static/` and `templates/` directories contain the necessary files (`style.css`, `script.js`, `index.html`).

### Steps to Run the Web Application

1. **Activate the Virtual Environment (if not already active):**

   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **On macOS and Linux:**
     ```bash
     source venv/bin/activate
     ```

2. **Start the FastAPI Server:**

   Ensure you're in the project root directory and run the following command:

   ```bash
   uvicorn main:app --reload
   ```

   - **Explanation:**
     - `main` refers to the `main.py` file.
     - `app` is the FastAPI instance defined in `main.py`.
     - `--reload` enables auto-reloading of the server on code changes (useful during development).

3. **Access the Web Application:**

   Open your web browser and navigate to:

   ```
   http://127.0.0.1:8000/
   ```

   You should see the **Nigerian House Price Prediction** interface where you can input house details and get a price prediction.

4. **Using the Application:**

   - **Input Fields:**
     - **Bedrooms**: Enter the number of bedrooms.
     - **Bathrooms**: Enter the number of bathrooms.
     - **Toilets**: Enter the number of toilets.
     - **Parking Space**: Enter the number of parking spaces.
     - **House Type**: Select the type of house from the dropdown menu.
     - **State**: Select the state where the house is located.
     - **Town**: Select the town based on the selected state.

   - **Predict Price:**
     After filling in all the required fields, click the **Predict Price** button. The predicted house price will be displayed below the form.

### Additional Notes

- **API Endpoints:**
  - `/states`: Retrieves the list of states.
  - `/towns/{state}`: Retrieves the list of towns for a given state.
  - `/house-types`: Retrieves the list of house types.
  - `/predict`: Accepts house details and returns the predicted price.

- **Static Files:**
  Ensure that the `static/` directory contains `style.css` and `script.js` for proper styling and functionality of the frontend.

- **Templates:**
  The `templates/` directory should contain the `index.html` file which serves as the frontend interface.

- **Model Files:**
  All trained model files (e.g., `ridge_reg.pkl`) and JSON files (`state_town_dict.json`, `house_title.json`) must be present in the `models/` directory for the application to function correctly.

### Troubleshooting

- **Port Already in Use:**
  If you encounter an error indicating that port `8000` is already in use, you can specify a different port:

  ```bash
  uvicorn main:app --reload --port 8001
  ```

- **Missing Dependencies:**
  Ensure all required Python packages are installed. If you encounter `ModuleNotFoundError`, verify your `requirements.txt` and install any missing packages:

  ```bash
  pip install -r requirements.txt
  ```

- **Model Loading Issues:**
  Ensure that all model `.pkl` files and JSON files are correctly placed in the `models/` directory. Check file paths in the `predict.py` and `main.py` files.

## Results

The best-performing models based on RMSE and R² were:

- **Random Forest Regressor**: After hyperparameter tuning, it provided the best balance of prediction accuracy and generalization.
- **XGBoost**: Also performed exceptionally well with slightly higher RMSE compared to the Random Forest model.

These models were serialized using Python's `pickle` module and are ready for deployment in the web application.

## Future Work

1. **Feature Importance**: Investigate feature importance to gain more insights into the most influential features.

2. **Additional Features**: Include additional geographical or economic data to enhance prediction accuracy.

3. **Web Deployment Enhancements**: Improve the web application's UI/UX and add more interactive features.

4. **Model Interpretation**: Use tools like SHAP or LIME to explain the model's predictions.

5. **Real-Time Data Updates**: Integrate real-time data feeds to keep the model updated with the latest housing trends.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to create a pull request. Please ensure that your contributions adhere to the project's coding standards and include appropriate documentation.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or feedback, please contact:

- **Email**: [aibard.annonymousasquare@gmail.com](aibard.annonymousasquare@gmail.com)
- **GitHub**: [aiBard](https://github.com/aiBard101/)
- **X**: [aiBard001](https://x.com/aiBard001)
- **Telegram**: [aiBard001](https://t.me/aiBard101)
- **LinkedIn**: [aiBard](https://www.linkedin.com/in/george-junior-alainengiya-5b44b5251/)
- **WhatsApp**: [aiBard](https://%20https://wa.me/message/AL5IJZCUYD6LG1)
- **Visit my Website**: [Website](https://aibard.code.blog/).

---
Watch the [YouTube video](https://youtu.be/G4SbqmyTak4) demonstrating the application.