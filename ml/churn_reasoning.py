import sqlite3
import pandas as pd
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
DB_PATH = os.path.join(DATA_DIR, 'enterprise_data.db')
INSIGHTS_PATH = os.path.join(DATA_DIR, 'ml_insights.json')

def analyze_churn():
    if not os.path.exists(DB_PATH):
        print("Database not found. Run data_generator.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('SELECT * FROM customer_metrics', conn)
    conn.close()

    print(f"Loaded {len(df)} rows for training.")

    # Preprocessing
    # Drop customerID
    X = df.drop(['customerID', 'Churn'], axis=1)
    y = df['Churn']

    # Handle Categoricals
    cat_cols = X.select_dtypes(include=['object']).columns
    le_dict = {}
    for col in cat_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        le_dict[col] = le

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluation
    accuracy = clf.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Feature Importance
    feature_importances = pd.DataFrame({
        'feature': X.columns,
        'importance': clf.feature_importances_
    }).sort_values('importance', ascending=False)

    top_features = feature_importances.head(5).to_dict('records')
    
    # Generate Insights
    high_risk_prob = clf.predict_proba(X)[:, 1]
    df['churn_probability'] = high_risk_prob
    high_risk_customers = df[df['churn_probability'] > 0.7] # High threshold
    
    # Segment Analysis: Who is high risk?
    # Simple aggregation on original df to find patterns in high risk
    # We use the original DF (before encoding) for readable insights, but we need to re-attach categorical values
    # Actually, let's just use the original df we loaded.
    
    df_high_risk = df.loc[high_risk_customers.index]
    
    # Find most common attribute in high risk group
    top_contract = df_high_risk['Contract'].mode()[0]
    top_internet = df_high_risk['InternetService'].mode()[0]
    avg_monthly = df_high_risk['MonthlyCharges'].mean()

    insights = {
        "summary": {
            "model_accuracy": f"{accuracy:.1%}",
            "total_customers": len(df),
            "overall_churn_rate": f"{y.mean():.1%}",
            "high_risk_customers_count": len(high_risk_customers)
        },
        "top_risk_factors": [
            {
                "feature": f.get("feature"),
                "importance": f"{f.get('importance'):.2f}"
            } for f in top_features
        ],
        "critical_segments": [
            {
                "segment_name": f"{top_contract} Users with {top_internet}",
                "risk_score": "Critical",
                "reasoning": f"This segment shows disproportionately high churn probability (>70%). Average monthly spend is ${avg_monthly:.2f}."
            }
        ],
        "recommendations_foundation": [
            f"Offer long-term contract incentives to {top_contract} users.",
            f"Review service quality for {top_internet} customers.",
            "Implement 'save-teams' for customers with Monthly Charges > $80."
        ]
    }

    with open(INSIGHTS_PATH, 'w') as f:
        json.dump(insights, f, indent=4)
    
    print(f"Real ML insights generated and saved to {INSIGHTS_PATH}")

if __name__ == "__main__":
    analyze_churn()
