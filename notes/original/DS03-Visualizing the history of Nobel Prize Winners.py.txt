#The Nobel Foundation has made a dataset available of all prize winners from the outset of the awards from 1901 to 2023. The dataset used in this project is from the Nobel Prize API and is available in the nobel.csv file in the data folder.

#In this project, you'll get a chance to explore and answer several questions related to this prizewinning data. And we encourage you then to explore further questions that you're interested in!

#1. What is the most commonly awarded gender and birth country?

    #Store your answers as string variables top_gender and top_country.
#2.Which decade had the highest ratio of US-born Nobel Prize winners to total winners in all categories?

    #Store this as an integer called max_decade_usa.
#3. Which decade and Nobel Prize category combination had the highest proportion of female laureates?

     #Store this as a dictionary called max_female_dict where the decade is the key and the category is the value. There should only be one key:value pair.
#4.Who was the first woman to receive a Nobel Prize, and in what category?

     #Save your string answers as first_woman_name and first_woman_category.
#5. Which individuals or organizations have won more than one Nobel Prize throughout the years?

    #Store the full names in a list named repeat_list.

# Loading in required libraries
import pandas as pd
import seaborn as sns
import numpy as np

# Start coding here!
df=pd.read_csv("data/nobel.csv")
print(df.columns)

#1
top_gender=df["sex"].mode([0])[0]
top_country=df["birth_country"].mode([0])[0]
print("answer1\n The gender with the most Nobel laureates is :", top_gender)
print(" The most common birth country of Nobel laureates is :", top_country)

#2
df["decade"] = (df["year"] // 10) * 10

each_decade= df["decade"].value_counts()

usa = df[df["birth_country"] == "United States of America"]
each_usa = usa["decade"].value_counts()

max_decade_usa = (each_usa / each_decade).idxmax() 
print("answer2\n The most common birth country of Nobel laureates is :" , max_decade_usa)

#3***********************************************************
# Calculating the proportion of female laureates per decade
nobel['female_winner'] = nobel['sex'] == 'Female'
prop_female_winners = nobel.groupby(['decade', 'category'], as_index=False)['female_winner'].mean()

# Find the decade and category with the highest proportion of female laureates
max_female_decade_category = prop_female_winners[prop_female_winners['female_winner'] == prop_female_winners['female_winner'].max()][['decade', 'category']]

# Create a dictionary with the decade and category pair
max_female_dict = {max_female_decade_category['decade'].values[0]: max_female_decade_category['category'].values[0]}

# Optional: Plotting female winners with % winners on the y-axis
#ax2 = sns.relplot(x='decade', y='female_winner', hue='category', data=prop_female_winners, kind="line")



#*********************

###3
each_female = (
    df[df["sex"] == "Female"]             # 先筛选出女性
    .groupby(["decade", "category"])      # 按 decade 和 category 分组
    .size()                               # 统计每组的数量
    .reset_index(name="female_count")     # 转成 DataFrame
)
each_sex = (
     df.groupby(["decade", "category"])
    .size()
    .reset_index(name="count")
)

prop_female = (                            #合并表格，缺数据的补齐为0
       each_sex
      .merge(each_female, on=["decade", "category"], how="left")
      .fillna({"female_count": 0})
)

prop_female["prop_female"] = prop_female["female_count"] / prop_female["count"]
max_female= prop_female[prop_female["prop_female"]==prop_female["prop_female"].max()]
max_female_dict = {max_female["decade"].values[0]: max_female["category"].values[0] }  ###.values[0]是很有用的,和iloc[0]的结果一样

# Optional: Plotting female winners with % winners on the y-axis
ax2 = sns.relplot(x='decade', y='prop_female', hue='category', data=prop_female, kind="line", marker="o")  #y轴直接用比列画
ax2.set(ylabel="Proportion of Female Winners", xlabel="Decade", title="Female Nobel Prize Winners Over Time")

print("answer3\n The decade and Nobel Prize category combination had the highest proportion of female laureates :" , max_female_dict)

#4
first_woman = (
    df[df["sex"] == "Female"]             # 先筛选出女性
    .sort_values(by=["year", "category"], ascending=True)
    .loc[:, ["full_name", "year", "category"]] 
    .reset_index(drop=True)     # 转成 DataFrame
)
print(first_woman)
first_woman_name = first_woman.iloc[0,0]
first_woman_category = first_woman.iloc[0,2]

print(f"answer4\n The first woman to win a Nobel Prize was {first_woman_name}, in the category of {first_woman_category}.")

#5 Selecting the laureates that have received 2 or more prizes
counts = nobel['full_name'].value_counts()         #确实我没搞懂为啥organization也出来了
repeats = counts[counts >= 2].index
repeat_list = list(repeats)

print("answer5\n The repeat winners are :", repeat_list)

##下面是我写的，但是个字典
#counts = nobel[["full_name", "organization_name"]].value_counts()
#repeat2=repeat[repeat["count"] >= 2].sort_values("count", ascending=False).reset_index(drop=True)
#repeat_list= repeat2.set_index("full_name")["organization_name"].to_dict()
#print("answer5\n", repeat_list)