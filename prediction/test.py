import requests
import json
import joblib as job
donnees={'PAY_AMT1':225.000000, 'PAY_AMT2':4019.000000, 'PAY_AMT3':4019.000000, 'PAY_AMT4':5000.000000, 'PAY_AMT5':5778.000000, 'PAY_AMT6':23978.000000, 'total_pay_amt':42860.000000, 'AVG_pay':7143.333333, 'LIMIT_BAL':300000.000000, 'total_bill_credit': 0.072286, 'PAY_1':-2.000000, 'PAY_2':-2.000000, 'PAY_3':-2.000000, 'PAY_4':-2.000000, 'PAY_5':-1.000000, 'PAY_6':-1.000000, 'retard':0.000000, 'AVG_delai':-1.666667, 'max_retard':-1.000000, 'avant':1.000000}
data={"LIMIT_BAL":300000.000000,
"SEX" :1.000000,
"EDUCATION" :1.000000,
"MARRIAGE" :1.000000,
"AGE": 47.000000,
"PAY_1" :-2.000000,
"PAY_2" :-2.000000,
"PAY_3":-2.000000,
"PAY_4" :-2.000000,
"PAY_5" :-1.000000,
"PAY_6" :-1.000000,
"BILL_AMT1" :0.000000,
"BILL_AMT2" :225.000000,
"BILL_AMT3" :4019.000000,
"BILL_AMT4" :4509.000000,
"BILL_AMT5" :7155.000000,
"BILL_AMT6" :5778.000000,
"PAY_AMT1":225.000000,
"PAY_AMT2":4019.000000,
"PAY_AMT3":3860.000000,
"PAY_AMT4" : 5000.000000,
"PAY_AMT5":5778.000000,
"PAY_AMT6" :23978.000000,
"pay_mt_trend":3576.628571,
"AVG_pay":7143.333333,
"retard":0.000000,
"AVG_delai" :-1.666667,
"max_retard":-1.000000,
"total_pay_amt":42860.000000,
"pay_to_credit" :0.142866,
"total_bill_amt":21686.000000,
"total_bill_credit": 0.072286,
 "avant":6.000000}
model_file="xboost.joblib"
url='http://127.0.0.1:5000'
model=requests.get(f"{url}/model")
if model.status_code==200:
   with open(model_file,"wb") as f:
      f.write(model.content)
   print("le model est chargé")
   print(job.load(model_file))
reponse=requests.post(f"{url}/predict",json=data)
try :
   result =reponse.json()
   print(result)
except Exception as e :
   print("erreur pour post")

