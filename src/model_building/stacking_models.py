import joblib
import pandas as pd
import numpy as np
import os
import pickle
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import KFold, TimeSeriesSplit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score


class Stacking:

    def __init__(self, base_models, meta_model, cv=5, pretrained=None):
        self.base_models = base_models
        self.meta_model = meta_model
        self.cv = cv
        if pretrained is None:
            self.pretrained = []
        else:
            self.pretrained = pretrained

    def fit(self, X, y):
        kf = KFold(n_splits=self.cv, shuffle=True, random_state=42)
        meta_features = np.zeros((X.shape[0], len(self.base_models)))

        for i, (name, model) in enumerate(self.base_models):
            if name in self.pretrained or i in self.pretrained:
                meta_features[:, i] = model.predict_proba(X)[:, 1]
                continue

            for train_idx, val_idx in kf.split(X):
                model.fit(X[train_idx], y[train_idx])
                meta_features[val_idx, i] = model.predict_proba(X[val_idx])[:, 1]

            model.fit(X, y)

        self.meta_model.fit(meta_features, y)
        return self

    def predict(self, X):
        meta_features = np.column_stack([model.predict_proba(X)[:, 1] for _, model in self.base_models])
        return self.meta_model.predict(meta_features)


class CoolStacking(Stacking):

    def __init__(self, base_models, meta_model, cv=5, sampling_strategy='auto', pretrained=None):
        super().__init__(base_models, meta_model, cv, pretrained)
        self.smote = SMOTE(sampling_strategy=sampling_strategy, random_state=42)

    def fit(self, X, y):
        X_resampled, y_resampled = self.smote.fit_resample(X, y)
        return super().fit(X_resampled, y_resampled)

    def evaluate(self, X, y):
        y_pred = self.predict(X)
        return {
            'accuracy': accuracy_score(y, y_pred),
            'f1_score': f1_score(y, y_pred, average='weighted'),
            'precision': precision_score(y, y_pred, average='weighted'),
            'recall': recall_score(y, y_pred, average='weighted')
        }


def main():
    print("Loading base models...")
    with open('../our_models/3__Xgboost__v1.pkl', 'rb') as f:
        xgb_model = pickle.load(f)
    with open('../our_models/3__RF__v1.pkl', 'rb') as f:
        rf_model = pickle.load(f)
    with open('../our_models/3__LightGBM__v1.pkl', 'rb') as f:
        lgb_model = pickle.load(f)

    print("Loading and preparing data...")
    df = pd.read_parquet('../../data/all_data_preprocessed/all_merged.parquet')
    X = df.drop(columns=[
        'event_all_region', 'alarms_in_regions', 'event_1h_ago',
        'event_2h_ago'])
    y = df['event_all_region']

    print("Splitting data...")
    tscv = TimeSeriesSplit(n_splits=5)
    splits = list(tscv.split(X))
    train_idx, test_idx = splits[-1]
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')

    print("Scaling data...")
    scaler = joblib.load('../our_models/scaler_v1.pkl')
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    base_models = [
        ('xgb', xgb_model),
        ('rf', rf_model),
        ('lgb', lgb_model)
    ]
    pretrained_models = ['xgb', 'rf', 'lgb']
    meta_model = LogisticRegression()

    print("Training stacking ensemble...")
    stacking_model = CoolStacking(
        base_models,
        meta_model,
        cv=5,
        pretrained=pretrained_models
    )
    stacking_model.fit(X_train_scaled, y_train)

    print("Evaluating model...")
    evaluation_results = stacking_model.evaluate(X_test_scaled, y_test)
    print("Imbalanced Stacking Classifier Results:")
    for metric, value in evaluation_results.items():
        print(f"{metric}: {value:.4f}")

    print("Saving model...")

    os.makedirs('../our_models', exist_ok=True)
    with open('../our_models/3__MUSE__v1.pkl', 'wb') as f:
        pickle.dump(stacking_model, f)

    return stacking_model, evaluation_results


if __name__ == "__main__":
    main()