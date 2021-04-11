import argparse
import pickle
from sklearn import tree
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor

def read_dataset(filename, feature_cols):
    df = pd.read_csv(filename)
    df.fillna(df.mean(), inplace=True)
    df = df.loc[:, feature_cols]
    return df

def dtrees(X_fit, y_fit, X_eval, y_eval, features, dt_file):
    #DTrees
    dtree = tree.DecisionTreeRegressor().fit(X_fit, y_fit)
    accuracy = dtree.score(X_eval, y_eval)
    dt_file.write(f'Single Dtree: {accuracy}\n')

    for feature, imp in zip(features, dtree.feature_importances_):
        dt_file.write("\tFeature %s: %s\n" % (feature, imp))

    pickle.dump(dtree, open('dtree.p', 'wb'))

    #Random Forest Trees
    rf_dtree = RandomForestRegressor(n_estimators=8).fit(X_fit,y_fit)
    accuracy = rf_dtree.score(X_eval,y_eval)
    dt_file.write(f'Random Forest Dtrees: {accuracy}\n')

    #Extremely Randomized Trees
    extra_rf_dtree = ExtraTreesRegressor(n_estimators=8).fit(X_fit,y_fit)
    accuracy = extra_rf_dtree.score(X_eval,y_eval)
    dt_file.write(f'Extremely Randomized Dtrees: {accuracy}\n')

    #Gradient Boosting Trees
    gb_tree = GradientBoostingRegressor(n_estimators=50, learning_rate=1.0, max_depth=2, random_state=0).fit(X_fit, y_fit)
    accuracy = gb_tree.score(X_eval, y_eval)
    dt_file.write(f'Gradient Boosting Dtrees: {accuracy}')

def runtime():
    parser = argparse.ArgumentParser(description='Fit & Score Dtree Regressors')
    parser.add_argument('-dcf', '--domestic_coffee_features', nargs='+', default=['domestic_consumption', '2018'],
                        help='the features from domestic coffee production to include')
    parser.add_argument('-icf', '--import_coffee_features', nargs='+', default=['imports', '2018'],
                        help='the features from foreign coffee import to include')
    parser.add_argument('-cf', '--covid_features', nargs='+', default=['Country', 'Positive/Tested %'],
                        help='the COVID-19 infection rates by country')
    # parser.add_argument('-hf', '--cheer_features', nargs='+', default=['Country', 'Score'],
    #                     help='happiness by country')
    parser.add_argument('-hf', '--cheer_features', nargs='+', default=['Country name', 'Ladder score'],
                        help='happiness by country')
    parser.add_argument('-tf', '--total_features', nargs='+', default=['Coffee Consumption', 'Positive/Tested %'],
                        help='total list of features')
    parser.add_argument('-ofn', '--outputfilename', default="output3")

    args = parser.parse_args()

    dcf = args.domestic_coffee_features
    icf = args.import_coffee_features
    cf = args.covid_features
    hf = args.cheer_features

    dcf_dataset = read_dataset('domestic-consumption.csv', dcf)
    dcf_dataset = dcf_dataset.rename(columns={"domestic_consumption": "Country", "2018": "Coffee Consumption"})
    icf_dataset = read_dataset('imports.csv', icf)
    icf_dataset = icf_dataset.rename(columns={"imports": "Country", "2018": "Coffee Consumption"})
    cf_dataset = read_dataset('TestsConducted_AllDates_13July2020.csv', cf)
    cf_dataset = cf_dataset.drop_duplicates(keep='last', ignore_index=True, subset=['Country'])
    # hf_dataset = read_dataset('WorldHappiness2018_Data.csv', hf)
    hf_dataset = read_dataset('world-happiness-report-2021.csv', hf)
    hf_dataset = hf_dataset.rename(columns={"Country name": "Country", "Ladder score": "Score"})

    full_dataset = dcf_dataset.append(icf_dataset, ignore_index=True)
    full_dataset = full_dataset.sort_values(by=['Country'])
    full_dataset = pd.merge(left=full_dataset, right=cf_dataset, left_on='Country', right_on='Country')
    full_dataset = pd.merge(left=full_dataset, right=hf_dataset, left_on='Country', right_on='Country')
    # full_dataset = pd.concat([full_dataset, cf_dataset, hf_dataset])
    # print(full_dataset)
    pickle.dump(full_dataset, open('full_dataset.p', 'wb'))

    features = args.total_features

    X = full_dataset[features]
    y = full_dataset['Score']

    X_fit, X_eval, y_fit, y_eval = train_test_split(X, y, test_size=0.30, random_state=2)
    dt_file = open(args.outputfilename + '.txt', 'w')
    dtrees(X_fit, y_fit, X_eval, y_eval, features, dt_file)

runtime()