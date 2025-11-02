#对数据进行探索性数据分析，netflix_data.csv以进一步了解 20 世纪 90 年代的电影。

#20 世纪 90 年代最常见的电影时长是多少？将近似答案保存为一个整数duration（以 1990 年作为该十年的起始年份）。

#如果一部电影少于 90 分钟，则被认为是短片。统计20 世纪 90 年代发行的短篇动作片short_movie_count的数量，并将该整数保存为。



# Importing pandas and matplotlib
import pandas as pd
import matplotlib.pyplot as plt

# Read in the Netflix CSV as a DataFrame
df = pd.read_csv("netflix_data.csv")

#print(df.info())
#print(df.head(10))
#print(df.describe())

#print(df.columns)
#df_movies= df[df['type']=='movie']

df_movies = df[df['type'].str.lower() == 'movie']

duration1=(df_movies['duration'].mode())
#print(duration1)
#print("#######")
df_90s = df_movies[(df_movies['release_year'] >= 1990) & (df_movies['release_year'] <= 1999)].copy()
duration=int(df_90s['duration'].mode()[0])
print("duration=",duration)

##(2)
#print(df_90s.head(10))
short_action = df_90s[(df_90s['duration'] < 90) & (df_90s['genre'].str.contains("Action", case=False, na=False))]
short_movie_count = short_action.shape[0]
print("short_movie_count=",short_movie_count)
