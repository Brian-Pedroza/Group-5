import pandas as pd
import matplotlib.pyplot as plt

# get data from csv
df = pd.read_csv('data/authors_touches.csv')
df['Date'] = pd.to_datetime(df['Date'], utc=True)

# get the week count
start_date = df['Date'].min()
df['weeks'] = (df['Date'] - start_date).dt.days / 7

# mapping each file to a number 
files = sorted(df['Filename'].unique())
file_map = {name: i for i, name in enumerate(files)}
df['file_index'] = df['Filename'].map(file_map)

authors = df['Author'].unique()

plt.figure(figsize=(12, 7))

# Draw the dots
for author in authors:
    author_data = df[df['Author'] == author]
    plt.scatter(author_data['file_index'], author_data['weeks'], label=author)

# lables
plt.title('Project Commits by Author')
plt.xlabel('file')
plt.ylabel('weeks')
# put legend on right side
plt.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize='small')
plt.tight_layout()

plt.savefig('data/Donald_scatterplot.png')
plt.show()