import csv
import datetime
import matplotlib.pyplot as plt

input_csv = "repo_mining/data/authors_file_touches_rootbeer.csv"

records = []
with open(input_csv) as f:
    reader = csv.DictReader(f)
    for row in reader:
        date = datetime.datetime.strptime(row["Date"], "%Y-%m-%dT%H:%M:%SZ")
        records.append((row["Filename"], row["Author"], date))

# Convert date → week number
base_date = min(r[2] for r in records)

points = []
for filename, author, date in records:
    week = (date - base_date).days // 7
    points.append((week, filename, author))

# Map files to index numbers (0,1,2,3…)
files = sorted(set(p[1] for p in points))
file_to_x = {f: i for i, f in enumerate(files)}

# Map authors to colors automatically
authors = sorted(set(p[2] for p in points))
cmap = plt.get_cmap("tab20", len(authors))
author_color = {a: cmap(i) for i, a in enumerate(authors)}

x = []
y = []
colors = []

for week, filename, author in points:
    x.append(file_to_x[filename])  # file index on x-axis
    y.append(week)                 # weeks on y-axis
    colors.append(author_color[author])

plt.figure()
plt.scatter(x, y, c=colors, s=60)

plt.xlabel("file")
plt.ylabel("weeks")

plt.savefig("repo_mining/scatterplot.png")
plt.close()

print("scatterplot.png created")
