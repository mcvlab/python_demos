# encoding: utf-8

import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset("iris")

# set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above)
sns.set(style="darkgrid")

# Create the plot
sns.histplot(data=df, y="sepal_length")
plt.show()

# set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above)
sns.set(style="darkgrid")

# Create the plot
sns.histplot(data=df, y="sepal_length", kde=True)
plt.show()
