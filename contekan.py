df['col_1'].unique()
df['col_1'].nunique()
df['col_1'].value_counts()


# apply function
def times2(x):
    return x*2
df['col_1'].apply(times2)

df['col_1'].apply(len)

# sorting
df.sort_values(by='col_1', inplace=True)

# cek null
df.isnull()

df.dropna()