import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.

    Agent: Actor
    State: list of (movie_id, person_id) pairs
    Action: 
    

    source_person = people[source]

    for movie in source_person.movies:
        actions = actions(movie)
"""
    frontier = QueueFrontier()

    for movie_stared in people[source]["movies"]:
        start = Node(state=(movie_stared, source), parent=None, action=None)
        frontier.add(start)

    explored = set()

    while True:
        if frontier.empty():
            return None
        
        node = frontier.remove()

        if is_goal(node.state, target):
            actions = []
            movie_people_pairs = []
            while node.parent is not None:
                #actions.append(node.action)
                movie_people_pairs.append(node.state)
                node = node.parent
            #actions.reverse()
            movie_people_pairs.reverse()
            return movie_people_pairs
        
        explored.add(node.state)

        (_, person_id) = node.state
        for state in neighbors_for_person(person_id):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=None)
                frontier.add(child)

    return None

def is_goal(state, target):
    (_, person_id) = state
    return person_id == target

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()

def goal_test(state, source, target):
    if len(state) < 2:
        return False
    if state[0].person_id == source and state[-1].person_id == target:
        return True
    else:
        return False
    
def get_actions(state):
    condition = lambda x: x != state.person_id
    neighbors = neighbors_for_person(state.person_id)
    return {x for x in neighbors if condition(x)}
    
class State():
    def __init__(self, movie_id, person_id):
        self.movie_id = movie_id
        self.person_id = person_id
