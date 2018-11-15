import random

random.seed()

maps = ['Germany', 'USA', 'India', 'China', 'Brazil']
tasks = ['Lookup', 'Detect change', 'Compare', 'Find top-k', 'Filter', 'Cluster', 'Find adjacency', 'Summarize']

questions = []


for mp in maps:

    for task in tasks:

        questions.append({'map': mp, 'task': task, 'taken': False})

questions_ordered = [{}]*len(questions)

for i in range(0, len(questions)):

    print("Selecting question {}...".format(i))

    random_id = random.randrange(0, len(questions))

    if i == 0:
        questions_ordered[i] = questions[random_id]
        questions[random_id]['taken'] = True
        continue
    
    while questions_ordered[i-1]['map'] == questions[random_id]['map'] or questions_ordered[i-1]['task'] == questions[random_id]['task'] or questions[random_id]['taken']:

        random_id = random.randrange(0, len(questions))
    
    questions_ordered[i] = questions[random_id]
    questions[random_id]['taken'] = True

for question in questions_ordered:
    print(question['map'])

print("")

for question in questions_ordered:
    print(question['task'])


