#Project Description
#Every year, school test results impact the college admissions fate of millions of students.

#In this project, you will use standardized test performance data from NYC's public schools to identify 
#the schools with top math results, look at how performance varies by borough, and find the city's top ten performing schools!

# Re-run this cell 
import pandas as pd

# Read in the data
schools = pd.read_csv("schools.csv")

# Preview the data
schools.head()

# Start coding here...

# Which schools are best for math?
best_math_schools = schools[schools["average_math"] >= 640][["school_name", "average_math"]].sort_values("average_math", ascending=False)

# Calculate total_SAT per school
schools["total_SAT"] = schools["average_math"] + schools["average_reading"] + schools["average_writing"]

# Who are the top 10 performing schools?
top_10_schools = schools.sort_values("total_SAT", ascending=False)[["school_name", "total_SAT"]].head(10)

# Which NYC borough has the highest standard deviation for total_SAT?
boroughs = schools.groupby("borough")["total_SAT"].agg(["count", "mean", "std"]).round(2)

# Filter for max std and make borough a column
largest_std_dev = boroughs[boroughs["std"] == boroughs["std"].max()]

# Rename the columns for clarity
largest_std_dev = largest_std_dev.rename(columns={"count": "num_schools", "mean": "average_SAT", "std": "std_SAT"})

# Optional: Move borough from index to column
largest_std_dev.reset_index(inplace=True)



###我写的question 1
best_math_schools = schools[schools["average_math"]>=640][["school_name","average_math"]].sort_values("average_math",ascending=False)


###quesiton 2
schools["total_SAT"]=schools["average_math"]+schools["average_reading"]+schools["average_writing"]
top_10_schools = (schools[["school_name","total_SAT"]].sort_values("total_SAT", ascending=False)).head(10)
                                                                 


#print(schools.iloc[:,4:7].head(5))
###question 3
boroughs = schools.groupby("borough")["total_SAT"].agg(num_schools="count",average_SAT="mean",std_SAT="std").round(2) #不能在这里排序只取一个后面写.head(1)
largest_std_dev = boroughs[boroughs["std_SAT"] == boroughs["std_SAT"].max()]
###change index to common columns
largest_std_dev.reset_index(inplace=True)
print(largest_std_dev.head())
