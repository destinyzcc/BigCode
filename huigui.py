import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm

data = pd.DataFrame({'avgscore': [93.53373879
    , 85.31361806
    , 75.20120806
    , 65.23313995
    , 47.31397473], 'submitscale': [0.946975461,
                                    0.887942846,
                                    0.848328374,
                                    0.681393955,
                                    0.628644501
                                    ], 'facescale': [0.119971878,
                                                     0.187736508,
                                                     0.250077375,
                                                     0.242900226,
                                                     0.207282343
                                                     ]}
                    )

data.head()

X = data['submitscale'].values.reshape(-1, 1)

y = data['avgscore'].values.reshape(-1, 1)

reg = LinearRegression()

reg.fit(X, y)

print("The linear model is: Y = {:.5} + {:.5}X".format(reg.intercept_[0], reg.coef_[0][0]))

predictions = reg.predict(X)

plt.figure(figsize=(16, 8))
plt.scatter(data['submitscale'], data['avgscore'], c='blue')
plt.plot(data['submitscale'], predictions, c='black', linewidth=2)
plt.ylabel("avgscore")
plt.xlabel("submitscale")
plt.show()

X = data['submitscale']
y = data['avgscore']

X2 = sm.add_constant(X)
est = sm.OLS(y, X2)
est2 = est.fit()
print(est2.summary())

Xs = data.drop(['avgscore'], axis=1)

y = data['avgscore'].values.reshape(-1, 1)

reg = LinearRegression()

reg.fit(Xs, y)

print("The linear model is: Y = {:.5} + {:.5}*submitscale + {:.5}*facescale ".format(reg.intercept_[0], reg.coef_[0][0],
                                                                                     reg.coef_[0][1]))

X = np.column_stack((data['submitscale'], data['facescale']))
y = data['avgscore']
X2 = sm.add_constant(X)
est = sm.OLS(y, X2)
est2 = est.fit()
print(est2.summary())
