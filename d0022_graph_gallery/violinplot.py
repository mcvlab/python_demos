# libraries & dataset
import seaborn as sns
import matplotlib.pyplot as plt

# set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above)
sns.set(style="darkgrid")
df = sns.load_dataset("iris")

# specifying the group list as 'order' parameter and plotting
sns.violinplot(
    x="species", y="sepal_length", data=df, order=["versicolor", "virginica", "setosa"]
)
plt.show()
