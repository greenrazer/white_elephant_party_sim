import math
import argparse
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

DEFAULT_NUMBER_OF_PARTICIPANTS = 3
DEFAULT_MAX_STEALS = 2

# print permutations of a given list 
# https://www.geeksforgeeks.org/generate-all-the-permutation-of-a-list-in-python/
def permutation(lst): 
    if len(lst) == 0: 
        return [] 

    if len(lst) == 1: 
        return [lst] 

    l = []
    for i in range(len(lst)): 
       m = lst[i] 
       remLst = lst[:i] + lst[i+1:] 
       for p in permutation(remLst): 
           l.append([m] + p) 
    return l 

class WhiteElephantAnalysis:

  def __init__(self, people, steals):
    self.people = people
    self.steals = steals
    self.gift_orderings = permutation(list(range(self.people)))
    self.curr_tree_info = {
      "gift_order": list(range(self.people)),
      "people_to_val": list(range(self.people)),
    }

  def run(self):
    outcomes = []
    for gift_order in self.gift_orderings:
      self.curr_tree_info["gift_order"] = gift_order
      outcomes.append(self.run_tree())


    partcipant_to_order_outcomes = [[0 for _ in range(self.people)] for _ in range(self.people)]
    
    for outcome in outcomes:
      for order in outcome:
        for gift, person in enumerate(order):
          partcipant_to_order_outcomes[person][gift] += 1

    total_entries = math.factorial(self.people)**2
    
    return partcipant_to_order_outcomes, total_entries



  def run_tree(self):
    for val, person in enumerate(self.curr_tree_info["gift_order"]):
      self.curr_tree_info["people_to_val"][person] = val
    
    outcomes = []
    self.run_tree_helper(
                    0,
                    [None for _ in range(self.people)],
                    [0 for _ in range(self.people)],
                    [None for _ in range(self.people)],
                    [],
                    None,
                    outcomes)
    return outcomes
    
  def run_tree_helper(self, 
                      turn,
                      gift_to_person, 
                      gift_to_steals,
                      person_to_gift,
                      no_steal,
                      steal, 
                      outcomes):
    # if past last turn
    if turn >= len(person_to_gift):
      outcomes.append(gift_to_person.copy())
      return
    
    curr_turn = turn if steal is None else steal
    # if can steal must steal
    must_steal = None
    person_val = self.curr_tree_info["people_to_val"][curr_turn]

    for gift_ind in range(person_val):
      if gift_to_person[gift_ind] is not None:
        if gift_to_steals[gift_ind] < self.steals:
          if gift_to_person[gift_ind] not in no_steal:
            must_steal = [gift_ind, gift_to_person[gift_ind]]
            break

    GIFT = 0
    PERSON = 1
    if must_steal:
      gift_to_person[must_steal[GIFT]] = curr_turn
      gift_to_steals[must_steal[GIFT]] += 1
      person_to_gift[curr_turn] = must_steal[GIFT]

      self.run_tree_helper(turn,
                            gift_to_person,
                            gift_to_steals, 
                            person_to_gift,
                            no_steal + [curr_turn],
                            must_steal[PERSON],
                            outcomes)
      gift_to_person[must_steal[GIFT]] = must_steal[PERSON]
      gift_to_steals[must_steal[GIFT]] -= 1
      person_to_gift[must_steal[PERSON]] = must_steal[GIFT]
    else:
      for gift_ind in range(self.people):
        if gift_to_person[gift_ind] is None:
          gift_to_person[gift_ind] = curr_turn
          person_to_gift[curr_turn] = gift_ind

          self.run_tree_helper(turn + 1,
                              gift_to_person, 
                              gift_to_steals,
                              person_to_gift, 
                              [],
                              None, 
                              outcomes)
          gift_to_person[gift_ind] = None
          person_to_gift[curr_turn] = None

def main():

  parser = argparse.ArgumentParser(description='Run white elephant analysis.')
  parser.add_argument('-n', '--number_of_participants', type=int, default=DEFAULT_NUMBER_OF_PARTICIPANTS, help='Number of participants in simulated white elephant party.')
  parser.add_argument('-s', '--graph_file', type=str, default=None, help='Save graph file.')
  parser.add_argument('-a', '--animation_file', type=str, default=None, help='Save rotation animation of graph.')
  parser.add_argument('-c', '--print_counts', action='store_true', help='Prints counts and total items.')
  parser.add_argument('-p', '--print_probabilities', action='store_true', help='Prints probabilities.')
  args = parser.parse_args()

  people = args.number_of_participants

  expected = [[0 for _ in range(people)] for _ in range(people)]

  for steals in range(people):
    white_elephant = WhiteElephantAnalysis(people,steals)
    counts, entries_per_row = white_elephant.run()

    if args.print_counts or args.print_probabilities:
      print()
      print(f'steals: {steals}')

    if args.print_counts:
      print('counts:')
      print(counts)
      print('row totals:')
      print(entries_per_row)

    if args.print_probabilities:
      probs = [row[:] for row in counts]
      for person in range(people):
        for gift in range(people):
          probs[person][gift] = counts[person][gift]/entries_per_row
      print("probabilities:")
      print(probs)

    for person in range(people):
      for gift in range(people):
        probability = counts[person][gift]/entries_per_row
        value =  people - (gift+1)
        expected[person][steals] += probability*value

  fig = plt.figure()
  ax = plt.axes(projection="3d")

  steal_axis = np.array(list(range(people)))
  people_axis = np.array(list(range(1,people+1)))

  X, Y = np.meshgrid(steal_axis, people_axis)
  Z = np.array(expected)

  if args.graph_file:
    ax.plot_surface(X, Y, Z, cmap='hot')
    ax.set_xticks(steal_axis)
    ax.set_yticks(people_axis)

    ax.set_zlim(0)

    ax.set_title(f'White Elephant Party With {people} Participants')
    ax.set_xlabel('Max Steals Per Gift')
    ax.set_ylabel('Participant')
    ax.set_zlabel('Expected Value Of Final Gift')
    plt.savefig(args.graph_file)

  if args.animation_file:
    def init():
      ax.plot_surface(X, Y, Z, cmap='hot')
      ax.set_xticks(steal_axis)
      ax.set_yticks(people_axis)

      ax.set_zlim(0)

      ax.set_title(f'White Elephant Party With {people} Participants')
      ax.set_xlabel('Max Steals Per Gift')
      ax.set_ylabel('Participant')
      ax.set_zlabel('Expected Value Of Final Gift')
      return fig,

    def animate(i):
        ax.view_init(elev=10., azim=i)
        return fig,

    # Animate
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=360, interval=20, blit=True)

    # Save
    anim.save(args.animation_file, writer='imagemagick', fps=30)


if __name__ == '__main__':
  main()