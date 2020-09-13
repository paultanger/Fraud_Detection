import pickle

class Predict():
    def __init__(self, filename='data/finalized_model.pkl'):
        self.loaded_model = pickle.load(open(filename, 'rb'))

    def _process_data(self, raw):
        df = pd.from_dict(raw, index_col=0)
        return self.vector.transform(df)

    def predict_from_raw(self, datain):
        processed = self._process_data(datain)
        probs = self.loaded_model.predict_proba(processed).flatten()
        return probs[1]

    def flag_label(self, row):
        if row['predict'] == 1 and row['predict'] > 0.97:
            return 'HIGH'
        elif row['predict'] > 0.95:
            return 'MEDIUM'
        elif row['predict'] > 0.91:
            return 'LOW'
        else:
            return 'Not Fraud'

if __name__ == "__main__":
    pass