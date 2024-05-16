import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


df = pd.read_csv('medical_examination.csv')


df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (df['bmi'] > 25).astype(int)
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


df['alcohol'] = (df['alco'] == 'yes').astype(int)


df_clean = df[
    (df['ap_lo'] <= df['ap_hi']) &
    (df['height'] >= df['height'].quantile(0.025)) &
    (df['height'] <= df['height'].quantile(0.975)) &
    (df['weight'] >= df['weight'].quantile(0.025)) &
    (df['weight'] <= df['weight'].quantile(0.975))
]

df_cat = pd.melt(df_clean, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'alco', 'active', 'smoke', 'overweight', 'alcohol'])

cat_plot = sns.catplot(
    x='variable',
    hue='value',
    col='cardio',
    data=df_cat,
    kind='count',
    height=5,
    aspect=0.7,
    order=['cholesterol', 'gluc', 'alco', 'active', 'smoke', 'overweight', 'alcohol'],
    palette="Set2"
)

cat_plot.set_axis_labels("variable", "total")
cat_plot.set_titles("{col_name} {col_var}")
cat_plot.set_xticklabels(['Normal', 'High'])

plt.show()

corr_matrix = df_clean.corr()

fig, ax = plt.subplots(figsize=(12, 10))


sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".1f",
    linewidths=.5,
    square=True,
    cmap="coolwarm",
    cbar_kws={"shrink": 0.8},
    mask=np.triu(corr_matrix)
)

plt.show()


print(f"BMI vs Cholesterol Correlation: {df_clean['bmi'].corr(df_clean['cholesterol'])}")


smoking_impact = df_clean[df_clean['smoke'] == 1].groupby('cardio')['cholesterol'].mean()
print(f"Average Cholesterol Level for Smokers with Cardiovascular Issues: {smoking_impact.mean()}")

plt.figure(figsize=(10, 6))
sns.violinplot(x='variable', y='bmi', data=df_clean, inner=None)
plt.title('Distribution of BMI Across Different Health Indicators')
plt.xlabel('Health Indicator')
plt.ylabel('BMI')
plt.xticks(rotation=45)
plt.show()
