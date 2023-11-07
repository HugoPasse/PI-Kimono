from src.utils.list_utils import sorted_arrays
from src.utils.proba_utils import pascal_triangle, proba_of_list

possibleDiceLaunches = [[]] + [sorted_arrays(0, 6, i) for i in range(1, 9)]
pascalTriangle = pascal_triangle(9)
launchProbability = []

for i in range(len(possibleDiceLaunches)):
    launchProbability.append([])
    for j in range(len(possibleDiceLaunches[i])):
        launchProbability[i].append(proba_of_list(possibleDiceLaunches[i][j], pascalTriangle))
        possibleDiceLaunches[i][j] = tuple(possibleDiceLaunches[i][j])
