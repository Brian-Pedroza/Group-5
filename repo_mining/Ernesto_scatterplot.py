import pandas as pd
import matplotlib.pyplot as plt

# get csv file into dataframe
df = pd.read_csv('data/rootbeer_author_touches.csv')

# convert date column to actual dates
df['Date'] = pd.to_datetime(df['Date'])

# starting date
start = df['Date'].min()
# last date
#last = df['Date'].max()

# calculate weeks
# get total seconds and convert it to weeks by dividing by 60 sec, 60 min, 24 hour and 7 days
df['WeeksFromStart'] = ((((((df['Date'] - start).dt.total_seconds()) / 60) / 60) /24) /7)

# create plot figure
plt.figure(figsize=(12,8))
# get unique authors
uniqueAuthors = df['Author'].unique()

df['FileNum'] = df['SrcFileName'].astype('category').cat.codes


# plot the graph
for authNum, auth in enumerate(uniqueAuthors):
    authinfo = df[df['Author'] == auth]
    plt.scatter(authinfo['FileNum'], authinfo['WeeksFromStart'], label=auth, s=50, edgecolors = 'black', linewidths = 0.5, alpha=0.5)

# matching labels format
plt.xlabel('Files', fontsize=14)
plt.ylabel('Weeks from start of the project', fontsize=14)
plt.title('Project Commits Authors and Timeline', fontsize=14)


plt.legend(bbox_to_anchor = (1,0.8), loc = 'upper left', title = 'Authors', fontsize= 8)
plt.grid(True, linestyle = ':', alpha = 0.3)

plt.savefig('rootbeer_author_touches_scatterplot.png')
plt.show()




