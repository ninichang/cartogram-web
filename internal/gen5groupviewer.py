import copy
import json
import os

# This function takes a fully-interactive question description
# for the cartogram viewing interface, and transforms it according
# to the given interactivity level.

def transform_viewer_question(question, level):

    new_question = {}

    if 'hide' in question:
        new_question['hide'] = question['hide']

    if question['type'] == "population":

        new_question['type'] = "population"
        new_question['map'] = question['map']
        new_question['interactive'] = {'deactivate': []}

        if level == 'none':
            new_question['interactive']['deactivate'] = ['tooltip', 'highlight', 'switching']
        
        if level == 'highlighting':
            new_question['interactive']['deactivate'] = ['tooltip', 'switching']
        
        if level == 'infotips':
            new_question['interactive']['deactivate'] = ['highlight', 'switching']
        
        if level == 'switching':
            new_question['interactive']['deactivate'] = ['tooltip', 'highlight']
    
    if question['type'] == "3switchable":

        new_question['type'] = "3maps"
        new_question['map'] = question['map']
        new_question['maps'] = question['maps']
        new_question['interactive'] = {'deactivate': []}

        if level == 'none':
            new_question['interactive']['deactivate'] = ['tooltip', 'highlight']
        
        if level == 'highlighting':
            new_question['interactive']['deactivate'] = ['tooltip']
        
        if level == 'infotips':
            new_question['interactive']['deactivate'] = ['highlight']
        
        if level == 'switching':
            new_question['type'] = "3switchable"
            new_question['interactive']['deactivate'] = ['tooltip', 'highlight']
    
    if question['type'] == "cartogram":

        new_question['type'] = "3maps"
        new_question['map'] = question['map']
        new_question['maps'] = [
            {'type': 'pregen', 'name': 'original'},
            {'type': 'data', 'name': question['data']},
            {'type': 'pregen', 'name': 'population'}
        ]
        new_question['interactive'] = {'deactivate': []}

        if level == 'none':
            new_question['interactive']['deactivate'] = ['tooltip', 'highlight']
        
        if level == 'highlighting':
            new_question['interactive']['deactivate'] = ['tooltip']
        
        if level == 'infotips':
            new_question['interactive']['deactivate'] = ['highlight']
        
        if level == 'switching':
            new_question['type'] = "3switchable"
            new_question['interactive']['deactivate'] = ['tooltip', 'highlight']
    
    return new_question

maps = ['Germany', 'USA', 'India', 'China', 'Brazil']
tasks = ['Lookup', 'Detect change', 'Compare', 'Find top-k', 'Filter', 'Cluster', 'Find adjacency', 'Summarize']

interactive_levels = ['none', 'highlighting', 'infotips', 'switching', 'all']

interactive_selector = 0

questions = []

randomized_maps = ['Brazil', 'Germany', 'Brazil', 'India', 'Germany', 'China', 'Germany', 'China', 'USA', 'India', 'Brazil', 'USA', 'China', 'USA', 'China', 'Germany', 'Brazil', 'China', 'Brazil', 'Germany', 'India', 'USA', 'India', 'USA', 'India', 'China', 'Brazil', 'USA', 'Germany', 'India', 'USA', 'Germany', 'India', 'Brazil', 'China', 'USA', 'Germany', 'China', 'India', 'Brazil']
randomized_categories = ['Cluster', 'Compare', 'Detect change', 'Lookup', 'Summarize', 'Detect change', 'Filter', 'Compare', 'Cluster', 'Filter', 'Find adjacency', 'Find top-k', 'Cluster', 'Compare', 'Find top-k', 'Find adjacency', 'Compare', 'Summarize', 'Lookup', 'Find top-k', 'Cluster', 'Summarize', 'Find adjacency', 'Lookup', 'Summarize', 'Lookup', 'Find top-k', 'Detect change', 'Cluster', 'Compare', 'Filter', 'Detect change', 'Find top-k', 'Summarize', 'Filter', 'Find adjacency', 'Lookup', 'Find adjacency', 'Detect change', 'Filter']

viewer_original = {}

with open('static/surveys/5groups-a/program.json', 'r') as jsonfile:
    viewer_original = json.load(jsonfile)

for i in range(len(randomized_maps)):

    questions.append({'map': randomized_maps[i], 'task': randomized_categories[i], 'group_levels': []})

# First we generate the interactivity levels

#for task in tasks:
#
    # For each group, the interactivity level is the same for all questions in the same task category.
#    group_levels = ['', '', '', '', '']
#
#    for i in range(5):
#
        #group_levels[i] = interactive_levels[(interactive_selector + i) % 5]
#    
    # Now search for questions with this task and set the interactivity levels
#
#    for question in questions:
#
#        if task == question['task']:
#            question['group_levels'] = copy.deepcopy(group_levels)
#    
#    interactive_selector += 1
#
#    print("""Task Type:\t{}
#Group 1:\t{}
#Group 2:\t{}
#Group 3:\t{}
#Group 4:\t{}
#Group 5:\t{}
#
#""".format(task, group_levels[0], group_levels[1], group_levels[2], group_levels[3], group_levels[4]))

for question in questions:

    for group in range(5):

        group_level = (tasks.index(question['task']) + maps.index(question['map']) + group) % 5

        question['group_levels'].append(interactive_levels[group_level])

# Generate the programs for each group

programs = [{'questions': []}, {'questions': []}, {'questions': []}, {'questions': []}, {'questions': []}]

for i in range(len(questions)):

    # This contains the fully interactive program
    original_program = viewer_original['questions'][i]

    for group in range(5):

        if questions[i]['group_levels'][group] == "all":
            programs[group]['questions'].append(original_program)
        else:
            programs[group]['questions'].append(transform_viewer_question(original_program, questions[i]['group_levels'][group]))

for group in range(5):

    if not os.path.isdir('static/surveys/5groups-{}'.format(group)):
        os.mkdir('static/surveys/5groups-{}'.format(group))
    
    with open('static/surveys/5groups-{}/program.json'.format(group), 'w') as programfile:
        json.dump(programs[group], programfile)

# Just report out for now

question_no = 1

for question in questions:

    print("""Question {}

Map:\t\t{}
Category:\t{}

Group 1:\t{}
Group 2:\t{}
Group 3:\t{}
Group 4:\t{}
Group 5:\t{}

""".format(question_no, question['map'], question['task'], question['group_levels'][0], question['group_levels'][1], question['group_levels'][2], question['group_levels'][3], question['group_levels'][4]))

    question_no += 1

for task in tasks:

    group_level_count = {'none': 0, 'highlighting':0, 'infotips':0, 'switching':0, 'all':0}

    for question in questions:

        if question['task'] == task:

            for group_level in question['group_levels']:

                group_level_count[group_level] += 1
    
    print("""Task Type:\t{}

none:\t\t{}
highlighting:\t{}
infotips:\t{}
switching:\t{}
all:\t\t{}

""".format(task, group_level_count['none'], group_level_count['highlighting'], group_level_count['infotips'], group_level_count['switching'], group_level_count['all']))

for group in range(5):

    group_level_count = {'none': 0, 'highlighting':0, 'infotips':0, 'switching':0, 'all':0}

    for question in questions:

        group_level_count[question['group_levels'][group]] += 1
    
    print("""Group {}

none:\t\t{}
highlighting:\t{}
infotips:\t{}
switching:\t{}
all:\t\t{}

""".format(group+1, group_level_count['none'], group_level_count['highlighting'], group_level_count['infotips'], group_level_count['switching'], group_level_count['all']))




