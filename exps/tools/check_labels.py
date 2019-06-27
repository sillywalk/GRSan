import pandas as pd
import sys
import comp_exp as ce
df = pd.read_csv(sys.argv[1])
df_l = ce.get_labeled(df)
print("labeled branches: "+str(len(df_l)))
