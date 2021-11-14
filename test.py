# import json

circles = []
music1 = ['Folk']
music2 = ['Techno/House']
p = 0

# json communities
'''with open('C:\\Users\\giorgos\\Desktop\\musae_git_features.json', 'r') as f:
    data = json.load(f)
for key, value in data.items():
    if len(value) > 35:
        value.insert(0, p)
        circles.append(value)
        p = p + 1
        # print(key, '-->', value)'''


# music communities
'''with open('C:\\Users\\giorgos\\Desktop\\HU_genres.json', 'r') as f:
    data = json.load(f)

for key, value in data.items():
    # print(key, '-->', value)
    for kind in value:
        if kind == 'Folk':
            music1.append(key)
        elif kind == 'Techno/House':
            music2.append(key)
circles.append(music1)
circles.append(music2)'''

# normal communities
with open('C:\\Users\\giorgos\\Desktop\\0.circles', 'r') as f:
    for line in f:
        k = line.split()
        circles.append(k)
        c = f.readline().split('\t')
        # print(c)
        c[-1] = c[-1].strip('\n')
        circles.append(c)

for circle in circles:
    print(circle)









