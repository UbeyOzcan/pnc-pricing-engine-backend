from src.ModelFactory import ModelFactory
from src.DataFactory import DataFactory


def main():
    DF = DataFactory()
    MF = ModelFactory(df=DF.getData().head(10000)) # train model on 10k data just to make our life easier on deployment as this is a demo model =)
    MF.frequency(expr="ClaimNb ~  Area + VehGas + VehAge + DrivAge")
    MF.severity(expr="ClaimAmount ~ VehPower + VehAge + DrivAge +  VehGas + Area")
    single_profile = {'VehPower': [10],
                      'VehAge': [0],
                      'DrivAge': [18],
                      #'BonusMalus': [50],
                      'VehGas': ['Regular'],
                      'Area': ['C']}
    rp = MF.riskpremium(env='prod', single_profile=single_profile)
    print(rp)

if __name__ == "__main__":
    main()
