# encoding: utf-8
# Libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

url = "https://raw.githubusercontent.com/holtzy/the-python-graph-gallery/master/static/data/email_campaign_funnel.csv"

# Original url (to be used in case the above one does not work)
url = "https://raw.githubusercontent.com/selva86/datasets/master/email_campaign_funnel.csv"
df = pd.read_csv(url)

# Create a figure and axis with a specific size
fig, ax = plt.subplots(figsize=(4, 8))

# Define the column in the dataframe that represents the groups/categories
group_col = "Gender"

# Determine the order of bars on the y-axis by unique values in the 'Stage' column and reversing the order
order_of_bars = df.Stage.unique()[::-1]

# Generate a list of colors for each group, using the Spectral colormap
colors = [
    plt.cm.Spectral(i / float(len(df[group_col].unique()) - 1))
    for i in range(len(df[group_col].unique()))
]

# Iterate through each group and plot a bar for each stage within that group
for color, group in zip(colors, df[group_col].unique()):
    # Create a bar plot using Seaborn's barplot function
    sns.barplot(
        x="Users",  # Data for the width of bars
        y="Stage",  # Data for the y-axis (stages of purchase)
        data=df.loc[df[group_col] == group, :],  # Filter data for the current group
        order=order_of_bars,  # Specify the order of stages on the y-axis
        color=color,  # Assign a color to the bar
        label=group,  # Assign a label for the plot legend
        ax=ax,  # Specify the axis to plot on (previously created)
    )

# Set labels and title for the axes
ax.set_xlabel("Users")  # X-axis label
ax.set_ylabel("Stage of Purchase")  # Y-axis label
ax.set_title("Population Pyramid of the Marketing Funnel", fontsize=22)  # Plot title

# Display the legend, which shows labels for the groups
ax.legend()

# Display the plot
plt.show()
