from backend.models.data import get_mtpl_data
import polars as pl
import xlsxwriter

# Building a normal one-way analysis that will help to build our picing model
# get the dataset
df = get_mtpl_data()

# data analysis for frequency modeling
###############################################
colnames = df.columns
X_colnames = [x for x in colnames if x not in ['IDpol', 'ClaimNb', 'Exposure', 'ClaimAmount']]

one_way = {}
wb = xlsxwriter.Workbook("oneway.xlsx",  {"nan_inf_to_errors": True})
for i in X_colnames:
    one_way[i] = df.group_by([i]).agg([pl.sum("Exposure").round(2), pl.sum("ClaimNb"), pl.sum("ClaimAmount").round(2)])
    one_way[i] = one_way[i].with_columns((pl.col("ClaimNb")/pl.col("Exposure")).alias('Frequency').round(4),
                                         (pl.col("ClaimAmount")/pl.col("ClaimNb")).alias('Severity').round(2))
    one_way[i] = one_way[i].with_columns((pl.col("Frequency") * pl.col('Severity')).alias('Risk Premium').round(2))
    one_way[i] = one_way[i].sort(i)
    one_way[i].write_excel(workbook=wb, worksheet=i)

wb.close()
