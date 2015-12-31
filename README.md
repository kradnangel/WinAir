# WinAir



## Statistic
Average age: 37

{'AU': 539,
'CA': 1428,
'DE': 1061,
'ES': 2249,
'FR': 5023,
'GB': 2324,
'IT': 2835,
'NDF': 124543,
'NL': 762,
'PT': 217,
'US': 62376,
'other': 10094}


## Log
1. Random Forest, n_estimators=100, n_jobs = -1, max_features = 'sqrt'

Training error 5.20548658286e-05

Validation error 0.407429963459

Testing score 0.65611

2. If the prediction is not 'NDF', add 'NDF' as the second prediction for this user.

Training error 2.08219463314e-05

Validation error 0.395483931416

Testing score 0.73602

## Submissions

### 1.

  #### Feature

  * All basic features
  * Converting date_account_created and date_first_booking into float

  #### Algorithm

  * Basic random forest, n_estimators=100, n_jobs = -1, max_features = 'sqrt'

  #### Result

  * Training error 0.00717316051118
  * Validation error 0.404384896468
  * Kaggle score: 0.73683


