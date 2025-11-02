#As a consultant working for a real estate start-up, you have collected Airbnb listing data from various sources to investigate the short-term rental market in New York. You'll analyze this data to provide insights on private rooms to the real estate company.

#There are three files in the data folder: airbnb_price.csv, airbnb_room_type.xlsx, airbnb_last_review.tsv.

#1What are the dates of the earliest and most recent reviews? Store these values as two separate variables with your preferred names.
#2How many of the listings are private rooms? Save this into any variable.
#3What is the average listing price? Round to the nearest two decimal places and save into a variable.
#4Combine the new variables into one DataFrame called review_dates with four columns in the following order: first_reviewed, last_reviewed, nb_private_rooms, and avg_price. The DataFrame should only contain one row of values.
################################我的答案################################################

price_df = pd.read_csv("data/airbnb_price.csv")
room_df = pd.read_excel("data/airbnb_room_type.xlsx")
review_df = pd.read_csv("data/airbnb_last_review.tsv", sep="\t")
#print(price_df.head())
#print(room_df.head())

print(review_df.head())
print(review_df.tail())
# 1. 提取时间部分
#小时分秒格式review_df['last_review'] = review_df['last_review'].dt.time

review_df['last_review'] = pd.to_datetime(review_df['last_review'], errors='coerce')
review_df['last_review'] = review_df['last_review'].dt.strftime('%Y%m%d')
review_df = review_df.sort_values('last_review', ascending=False)






first_reviewed = review_df['last_review'].min()
print("the dates of the earliest reviews：", first_reviewed)
last_reviewed = review_df['last_review'].max()
print("the dates of the most recent reviews：", last_reviewed)

###2
room_df['room_type']= room_df['room_type'].str.lower().str.strip()
#pri= room_df[room_df['room_type'] == 'private room'].count()
nb_private_rooms= len(room_df[room_df['room_type'] == 'private room'].value_counts())      # 打印行数（数量）
##也可以用.shape[0])       
# 或者
print(nb_private_rooms) 
###3
price_df['price']=price_df['price'].replace(r'[A-Za-z]', '', regex=True).str.strip()
price_df['price'] = pd.to_numeric(price_df['price'], errors='coerce')
avg_price=round(price_df['price'].mean(), 2)
print("the average listing price is：",avg_price,"dollars.")
#print(f"The average listing price is: {price_mean} dollars.")

###4
review_dates = pd.DataFrame({
    "first_reviewed": [first_reviewed],
    "last_reviewed": [last_reviewed],
    "nb_private_rooms": [nb_private_rooms],
    "avg_price": [avg_price]
})
print(review_dates)


########################################################################################
the dates of the earliest reviews： 2019-01-01
the dates of the most recent reviews： 2019-07-09
11346
the average listing price is： 141.78 dollars.
####################################################################################
#################################标准答案############################################


# Import CSV for prices
airbnb_price = pd.read_csv('data/airbnb_price.csv')

# Import Excel file for room types
airbnb_room_type = pd.read_excel('data/airbnb_room_type.xlsx')

# Import TSV for review dates
airbnb_last_review = pd.read_csv('data/airbnb_last_review.tsv', sep='\t')

# Join the three data frames together into one
listings = pd.merge(airbnb_price, airbnb_room_type, on='listing_id')
listings = pd.merge(listings, airbnb_last_review, on='listing_id')

# What are the dates of the earliest and most recent reviews?
# To use a function like max()/min() on last_review date column, it needs to be converted to datetime type
listings['last_review_date'] = pd.to_datetime(listings['last_review'], format='%B %d %Y')
first_reviewed = listings['last_review_date'].min()
last_reviewed = listings['last_review_date'].max()

# How many of the listings are private rooms?
# Since there are differences in capitalization, make capitalization consistent
listings['room_type'] = listings['room_type'].str.lower()
private_room_count = listings[listings['room_type'] == 'private room'].shape[0]

# What is the average listing price?
# To convert price to numeric, remove " dollars" from each value
listings['price_clean'] = listings['price'].str.replace(' dollars', '').astype(float)
avg_price = listings['price_clean'].mean()

review_dates = pd.DataFrame({
    'first_reviewed': [first_reviewed],
    'last_reviewed': [last_reviewed],
    'nb_private_rooms': [private_room_count],
    'avg_price': [round(avg_price, 2)]
})

print(review_dates)