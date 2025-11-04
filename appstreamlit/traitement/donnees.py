import pandas as pd
import pandas as pd
import numpy as np

class analyse:
    def __init__(self) -> None:
        self.df = pd.DataFrame()

    # Importer le dataset et nettoyer
    def dataset(self, path: str):
        try:
            self.df = pd.read_excel(path, header=1)
            self.df.rename({'PAY_0': 'PAY_1'}, inplace=True, axis=1)
            self.df.drop("ID", axis=1, inplace=True)
            self.df.drop_duplicates(inplace=True)
            return self.df
        except Exception as e:
            print(f"Erreur lors du chargement du dataset : {e}")
            return None

    # Création de nouvelles variables/features
    def feature_eng(self):
        df = self.df.copy()
        col_pay = [f"PAY_AMT{i}" for i in range(1, 7)]
        col_bill = [f"BILL_AMT{i}" for i in range(1, 7)]
        retard = [f"PAY_{i}" for i in range(1, 7)]

        df["pay_mt_trend"] = df[col_pay].apply(lambda x: np.polyfit(range(1, 7), x, 1)[0], axis=1)
        df["AVG_pay"] = df[col_pay].mean(axis=1)
        df["retard"] = df[retard].apply(lambda x: (x > 0).sum(), axis=1)
        df["AVG_delai"] = df[retard].mean(axis=1)
        df["max_retard"] = df[retard].max(axis=1)
        df["non_retard"] = df[retard].lt(0).sum(axis=1)
        df["total_pay_amt"] = df[col_pay].sum(axis=1)
        df["pay_to_credit"] = df["total_pay_amt"] / (df["LIMIT_BAL"] + 1)
        df["total_bill_amt"] = df[col_bill].sum(axis=1)
        df["total_bill_credit"] = df["total_bill_amt"] / (df["LIMIT_BAL"] + 1)

        columns = [
            "pay_mt_trend", "AVG_pay", "retard", "AVG_delai", "max_retard",
            "non_retard", "total_pay_amt", "pay_to_credit", "total_bill_amt",
            "total_bill_credit", "default payment next month", "SEX", "EDUCATION", "MARRIAGE"
        ]
        return df[columns]

    
        
    

