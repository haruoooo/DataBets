import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np

bets = pd.read_json('bets.json')
dados = pd.read_json('logs/registros.json')
teste = dados.tail(1)  

X = bets.drop(['aposta_fast'], axis=1)
y = bets['aposta_fast']

X['valor_aposta'] = np.log1p(X['valor_aposta'])
teste['valor_aposta'] = np.log1p(teste['valor_aposta'])

x_dummies = pd.get_dummies(X, columns=['time'], dtype=int)
teste = pd.get_dummies(teste, columns=['time'], dtype=int)
teste = teste.reindex(columns=x_dummies.columns, fill_value=0)

X_train, _, y_train, _ = train_test_split(x_dummies, y, test_size=0.2, random_state=42, stratify=y)
clf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
clf.fit(X_train, y_train)

prediction = clf.predict(teste)
print(int(prediction[0]))  
