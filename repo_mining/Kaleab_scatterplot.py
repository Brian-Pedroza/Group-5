import csv
import matplotlib.pyplot as plt

filePath = "../data/rootbeer_authors_touches.csv"
imagePath = "../data/kaleab_scatterplot.png"

weeks = []
files = []
authors = []

fileMap = {}
fileCounter = 0

with open(filePath, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        week = int(row["Week"])
        name = row["Filename"]
        author = row["Author"]

        if name not in fileMap:
            fileMap[name] = fileCounter
            fileCounter += 1

        weeks.append(week)
        files.append(fileMap[name])
        authors.append(author)

# create color mapping for authors
uniqueAuthors = list(set(authors))
authorMap = {}
for i in range(len(uniqueAuthors)):
    authorMap[uniqueAuthors[i]] = i

colors = []
for a in authors:
    colors.append(authorMap[a])

plt.figure(figsize=(12, 6))
plt.scatter(weeks, files, c=colors, cmap="tab20", s=10)

plt.xlabel("Week Number")
plt.ylabel("File Number")
plt.title("Rootbeer File Activity by Author")

plt.colorbar(label="Author Index")

plt.tight_layout()
plt.savefig(imagePath)
plt.show()

print("Scatterplot saved to:", imagePath)
