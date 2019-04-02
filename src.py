import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

health_data = pd.read_csv('train_2v.csv')
test_data = pd.read_csv('test_2v.csv')
health_data = health_data.dropna()
test_data = test_data.dropna()

# print(health_data.count())
# print(test_data.count())

X = health_data.drop(['id', 'heart_disease', 'work_type', 'stroke'], axis =1)
test_x = test_data.drop(['id', 'heart_disease', 'work_type'], axis = 1)
y = health_data.heart_disease
test_y = test_data.heart_disease


print(X.smoking_status.unique())

gender_dict = {'Male' : 0, 'Other' : 1, 'Female' : 2}
married_dict = {'No' : 0, 'Yes' : 1}
residence_type_dict = {'Rural' : 0, 'Urban' : 1}
smoker_type_dict = {'never smoked' : 0, 'formerly smoked' : 1, 'smokes' : 2}


X.gender = [gender_dict[item] for item in X.gender]
X.ever_married = [married_dict[item] for item in X.ever_married]
X.Residence_type = [residence_type_dict[item] for item in X.Residence_type]
X.smoking_status = [smoker_type_dict[item] for item in X.smoking_status]

test_x.gender = [gender_dict[item] for item in test_x.gender]
test_x.ever_married = [married_dict[item] for item in test_x.ever_married]
test_x.Residence_type = [residence_type_dict[item] for item in test_x.Residence_type]
test_x.smoking_status = [smoker_type_dict[item] for item in test_x.smoking_status]


hd_model = DecisionTreeRegressor()
hd_model.fit(X, y)

predictions =  hd_model.predict(test_x)
print(mean_absolute_error(test_y, predictions))

nr_ghici = 0
nr_cont = 0
nr_bol = 1
fal_pos = 0

keylist = list()
for key, value in test_y.iteritems():
    if value == 1:
        nr_bol+=1
        if predictions[nr_cont] == value:
            nr_ghici+=1
    if value == 0 and predictions[nr_cont] == 1:
        fal_pos += 1
    nr_cont+=1
    

print(str(nr_ghici) + ' din ' + str(nr_bol))
print('False positive:  ' + str(fal_pos))