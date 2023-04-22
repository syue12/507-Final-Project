# %%
import json
import networkx as nx
from networkx.readwrite import json_graph

# %% selected affiliations, personalities, and popularity used in the graphs
affiliations = ['Hogwarts School Of Witchcraft And Wizardry', 'Order Of The Phoenix', 
                "Dumbledore's Army", 'Gryffindor', 'Weasley Family', 'Lord Voldemort',
                'Slytherin', 'Hufflepuff']

personalisies = ['Brave', 'Loyal', 'Caring', 'Friendly', 'Protective', 'Evil', 
                 'Intelligent', 'Cruel', 'Kind', 'Murderous', 'Arrogant', 'Manipulative',
                 'Cold', 'Sadistic']

popularity = ['Millions', '100K', '10K', '1K', 'Hundreds']

# %% load the cleaned cached data
with open('hp_json.json') as f:
    hp = json.loads(f.read())

# %% to save the networkx graph as json graph file
# input: Graph, string
# output: json file
def saveGraph(G,filename):
    data = json_graph.node_link_data(G)
    with open(f'{filename}_graph.json', 'w') as outfile:
        json.dump(data, outfile)

# %% create and save the HP universe garph
HP_Universe = nx.Graph()

for character in hp:
    HP_Universe.add_node(character["name"])

for character in hp:
    for friend in character["friends"]:
        if friend != "none":
            HP_Universe.add_edge(character["name"], friend, relationship="friend")
    for enemy in character["enemies"]:
        if enemy != "none": 
            HP_Universe.add_edge(character["name"], enemy, relationship="enemy")

saveGraph(HP_Universe, "hp_universe")

# %% create and save the series graph
Series = nx.Graph()
for character in hp:
    Series.add_node(character["name"])
Series.add_node("Harry Potter Series")
Series.add_node("Fantastic Beasts Series")

for character in hp:
    if "Harry" in character["series"]:
        Series.add_edge(character["name"], "Harry Potter Series", relationship="series")
    if "Fantastic" in character["series"]:
        Series.add_edge(character["name"], "Fantastic Beasts Series", relationship="series")

saveGraph(Series, "hp_series")

# %% create and save the alignment graph
Alignment = nx.Graph()
for character in hp:
    Alignment.add_node(character["name"])
Alignment.add_node("Good")
Alignment.add_node("Bad")
Alignment.add_node("Complex")
Alignment.add_node("Neutral")

for character in hp:
    if character["alignment"] == "Good":
        Alignment.add_edge(character["name"], "Good", relationship="alignment")
    elif character["alignment"] == "Bad":
        Alignment.add_edge(character["name"], "Bad", relationship="alignment")
    elif character["alignment"] == "Complex":
        Alignment.add_edge(character["name"], "Complex", relationship="alignment")
    elif character["alignment"] == "Neutral":
        Alignment.add_edge(character["name"], "Neutral", relationship="alignment")

saveGraph(Alignment, "hp_align")

# %% create and save the personality graph
Personality = nx.Graph()
for character in hp:
    Personality.add_node(character["name"])
for personality in personalisies:
    Personality.add_node(personality)

for character in hp:
    for personality in character["personality"]:
        if personality.title() in Personality:
            Personality.add_edge(character["name"], personality.title(), relationship="personality")

saveGraph(Personality, "hp_personality")

# %% create and save the affiliation graph
Affiliations = nx.Graph()
for character in hp:
    Affiliations.add_node(character["name"])
for affiliation in affiliations:
    Affiliations.add_node(affiliation)

for character in hp:
    for affiliation in character["affiliations"]:
        if affiliation.title() in Affiliations:
            Affiliations.add_edge(character["name"], affiliation.title(), relationship="affiliation")

saveGraph(Affiliations, "hp_affiliation")

# %% create and save the popularity graph
Popularity = nx.Graph()
for character in hp:
    Popularity.add_node(character["name"])
for number in popularity:
    Popularity.add_node(number)

for character in hp:
    if character["popularity"] == 5:
        Popularity.add_edge(character["name"], "Millions", relationship="popularity")
    elif character["popularity"] == 4:
        Popularity.add_edge(character["name"], "100K", relationship="popularity")
    elif character["popularity"] == 3:
        Popularity.add_edge(character["name"], "10K", relationship="popularity")
    elif character["popularity"] == 2:
        Popularity.add_edge(character["name"], "1K", relationship="popularity")
    elif character["popularity"] == 1:
        Popularity.add_edge(character["name"], "Hundreds", relationship="popularity")

saveGraph(Popularity, "hp_popularity")