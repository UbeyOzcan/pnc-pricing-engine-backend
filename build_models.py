from src.ModelFactory import ModelFactory
from src.DataFactory import DataFactory


def main():
    DF = DataFactory()
    MF = ModelFactory(df=DF.getData().head(1000))
    MF.frequency(expr="ClaimNb ~  Area + VehGas + VehAge + DrivAge + VehBrand + BonusMalus + Density")
    MF = ModelFactory(df=DF.getData())
    MF.severity(expr="ClaimAmount ~ Area + VehGas + VehAge + DrivAge + VehBrand + BonusMalus + Density")
    single_profile = {'VehPower': [50],
                      'VehAge': [0],
                      'DrivAge': [50],
                      'BonusMalus': [90],
                      'VehGas': ['Regular'],
                      'Area': ['C'],
                      'Density': [2000],
                      'VehBrand': ['B12']}
    rp = MF.riskpremium(env='prod', single_profile=single_profile)
    print(rp)

if __name__ == "__main__":
    main()
