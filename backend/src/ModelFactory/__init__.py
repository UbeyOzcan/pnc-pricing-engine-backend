import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import joblib
from backend.src.DataFactory import DataFactory

DF = DataFactory()


class ModelFactory:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def frequency(self, expr: str):
        train, test = train_test_split(self.df, test_size=0.3, random_state=1990)
        train = self.df.loc[train.index].copy()
        train['Area'] = pd.Categorical(train['Area'], train.Area.value_counts().index)
        train['VehGas'] = pd.Categorical(train['VehGas'], train.VehGas.value_counts().index)
        # expr = "ClaimNb ~ VehPower + VehAge + DrivAge + BonusMalus  + VehGas + Area "
        FreqPoisson = smf.glm(formula=expr,
                              data=train,
                              offset=np.log(train['Exposure']),
                              family=sm.families.Poisson(link=sm.families.links.log())).fit()
        joblib.dump(FreqPoisson, f'{DF.get_project_root()}/models/prod/Frequency.joblib')

    def severity(self, expr: str):
        df = self.df[(self.df.ClaimNb > 0) & (self.df.ClaimNb < 5)]
        df['Severity'] = df.ClaimAmount / df.ClaimNb
        # frequency train test
        train, test = train_test_split(df, test_size=0.3, random_state=1990)
        train = df.loc[train.index].copy()
        SevGamma = smf.glm(formula=expr,
                           data=train,
                           offset=train.ClaimNb,
                           family=sm.families.Gamma(link=sm.families.links.log())).fit()

        joblib.dump(SevGamma, f'{DF.get_project_root()}/models/prod/Severity.joblib')

    def riskpremium(self, env: str, single_profile: dict):
        VALID_STATUS = {'prod', 'dev'}
        if env not in VALID_STATUS:
            raise ValueError("results: status must be one of %r." % VALID_STATUS)
        frequency = joblib.load(f'{DF.get_project_root()}/models/{env}/Frequency.joblib')
        severity = joblib.load(f'{DF.get_project_root()}/models/{env}/Severity.joblib')

        single_profile = pd.DataFrame.from_dict(single_profile)
        single_profile['expected_freq'] = round(frequency.predict(single_profile), 4)
        single_profile['expected_sev'] = round(severity.predict(single_profile), 2)

        single_profile['RP'] = round(single_profile['expected_freq'] * single_profile['expected_sev'], 2)
        single_profile = single_profile.to_dict('list')
        return single_profile
