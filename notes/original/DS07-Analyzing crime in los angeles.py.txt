#Explore the crimes.csv dataset and use your findings to answer the following questions:

#1. Which hour has the highest frequency of crimes? Store as an integer variable called peak_crime_hour.

#2. Which area has the largest frequency of night crimes (crimes committed between 10pm and 3:59am)? 
#Save as a string variable called peak_night_crime_location.

#3. Identify the number of crimes committed against victims of different age groups. 
#Save as a pandas Series called victim_ages, with age group labels "0-17", "18-25", "26-34", "35-44", 
#"45-54", "55-64", and "65+" as the index and the frequency of crimes as the values.

# Start coding here
# Use as many cells as you need
#1
crimes['hour'] = crimes['TIME OCC'].astype(int) // 100
peak_crime_hour= crimes['hour'].value_counts(ascending=False).idxmax()
print(peak_crime_hour)

#2确保TIME OCC是整数（有时候读入是字符串）
crimes['TIME OCC'] = crimes['TIME OCC'].astype(int)
# 提取晚上10点到凌晨3:59的犯罪记录
night_crimes = crimes[(crimes['TIME OCC'] >= 2200) | (crimes['TIME OCC'] < 400)]
#print(night_crimes.head())
peak_night_crime_location = night_crimes.groupby('AREA NAME').size().sort_values(ascending=False).index[0]
)
print(peak_night_crime_location)

#3
bins = [0, 17, 25, 34, 44, 54, 64, 120]
labels = ["0-17", "18-25", "26-34", "35-44", "45-54", "55-64", "65+"]

# 2. 按年龄区间分组并统计频数
victim_ages = pd.cut(crimes['Vict Age'], bins=bins, labels=labels, right=True).value_counts().sort_index()

# 3. 查看结果
print(victim_ages)




 ##标准答案：
 ## Which hour has the highest frequency of crimes? Store as an integer variable called peak_crime_hour

# Extract the first two digits from "TIME OCC", representing the hour,
# and convert to integer data type##取时间的前两个字符
crimes["HOUR OCC"] = crimes["TIME OCC"].str[:2].astype(int)  

# Preview the DataFrame to confirm the new column is correct
crimes.head()

# Produce a countplot to find the largest frequency of crimes by hour
sns.countplot(data=crimes, x="HOUR OCC")
plt.show()

# Midday has the largest volume of crime
peak_crime_hour = 12

## Which area has the largest frequency of night crimes (crimes committed between 10pm and 3:59am)? 
## Save as a string variable called peak_night_crime_location
# Filter for the night-time hours
# 0 = midnight; 3 = crimes between 3am and 3:59am, i.e., don't include 4
night_time = crimes[crimes["HOUR OCC"].isin([22,23,0,1,2,3])]

# Group by "AREA NAME" and count occurrences, filtering for the largest value and saving the "AREA NAME"
peak_night_crime_location = night_time.groupby("AREA NAME", 
                                               as_index=False)["HOUR OCC"].count().sort_values("HOUR OCC",
                                                                                               ascending=False).iloc[0]["AREA NAME"]
# Print the peak night crime location
print(f"The area with the largest volume of night crime is {peak_night_crime_location}")

## Identify the number of crimes committed against victims by age group (0-17, 18-25, 26-34, 35-44, 45-54, 55-64, 65+) 
## Save as a pandas Series called victim_ages
# Create bins and labels for victim age ranges
age_bins = [0, 17, 25, 34, 44, 54, 64, np.inf]
age_labels = ["0-17", "18-25", "26-34", "35-44", "45-54", "55-64", "65+"]

# Add a new column using pd.cut() to bin values into discrete intervals
crimes["Age Bracket"] = pd.cut(crimes["Vict Age"],
                               bins=age_bins,
                               labels=age_labels)

# Find the category with the largest frequency
victim_ages = crimes["Age Bracket"].value_counts()
print(victim_ages)