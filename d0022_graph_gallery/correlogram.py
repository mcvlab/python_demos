# encoding: utf-8

# library & dataset
import matplotlib.pyplot as plt
import seaborn as sns

df = sns.load_dataset("iris")

# with regression
sns.pairplot(df, kind="reg")
plt.show()

# without regression
sns.pairplot(df, kind="scatter")
plt.show()
