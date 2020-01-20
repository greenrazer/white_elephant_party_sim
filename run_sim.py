import numpy as np
import matplotlib.pylab as plt

class WhiteElephantSim:
  def __init__(self, number_of_participants, number_of_steals):
    self.revealed_presents = []
    self.unrevealed_presents = []
    self.presents = []
    self.people = []

    self.turn = 0
    self.steal_stack = []
    self.cant_steal = []

    self.number_of_steals = number_of_steals
    self.number_of_participants = number_of_participants

    self.generate_participants_normal()

  def generate_participants_normal(self, nmean = 0.5, nstd = 0.2):
    values = np.random.normal(nmean, nstd, self.number_of_participants)
    for i, val in enumerate(values):
      self.presents.append({
        'value': val,
        'steals': 0,
        'belongs_to': -1,
      })
      self.people.append({
        'threshold': val
      })
      self.unrevealed_presents.append(i)

  def run(self):
    while len(self.steal_stack) > 0 or self.turn < self.number_of_participants:
      self.step()
  
  def step(self):
    turn_user = self.turn
    if len(self.steal_stack):
      turn_user = self.steal_stack.pop()
    else:
      self.cant_steal = []
      self.turn += 1
    pick_or_steal = self.pick_or_steal(turn_user)
    if pick_or_steal > -1:
      self.steal_present(turn_user, pick_or_steal)
    else:
      self.pick_from_pile(turn_user)

  def pick_from_pile(self, to_id):
    if len(self.unrevealed_presents) == 0:
      raise Exception("Trying to pick from empty pile")
    picked = self.unrevealed_presents.pop()
    self.presents[picked]['belongs_to'] = to_id
    self.revealed_presents.append(picked)
    return picked
  
  def steal_present(self, user_id, present_id):
    if user_id < 0 or user_id >= self.number_of_participants:
      raise Exception("user_id not found")
    if present_id not in self.revealed_presents:
      raise Exception("present not stealable")
    if self.presents[present_id]['steals'] >= self.number_of_steals:
      raise Exception("number of steals exceeded")
    if present_id in self.cant_steal:
      raise Exception("cannot steal back present that has been stolen")

    new_turn = self.presents[present_id]['belongs_to']
    self.presents[present_id]['belongs_to'] = user_id
    self.presents[present_id]['steals'] += 1
    self.cant_steal.append(present_id)
    self.steal_stack.append(new_turn)

  def pick_or_steal(self, user_id):
    threshold = self.people[user_id]['threshold']
    curr_max = None
    max_ind = -1
    for p in self.revealed_presents:
      val = self.presents[p]['value']
      if val > threshold and (curr_max is None or val > curr_max):
        if self.presents[p]['steals'] < self.number_of_steals:
          if p not in self.cant_steal:
            curr_max = val
            max_ind = p

    return max_ind

  def get_relative_values(self):
    out = {}
    for present in self.presents:
      person = present['belongs_to']
      out[person] = present['value'] - self.people[person]['threshold']
    return out
  
  def get_values(self):
    out = {}
    for present in self.presents:
      person = present['belongs_to']
      out[person] = present['value']
    return out

  def get_people_present_pairs(self):
    out = []
    for i, present in enumerate(self.presents):
      out.append((present['belongs_to'], i))
    return out

def save_graph_return(filename, data, folder_path):
  plt.clf()
  data = sorted(data.items())
  x,y = zip(*data)
  axes = plt.gca()
  axes.set_ylim([-0.50 , 0.50])
  plt.plot(x,y)
  plt.savefig(f'{folder_path}/{filename}.png')

def save_graph_value(filename, data, folder_path):
  plt.clf()
  data = sorted(data.items())
  x,y = zip(*data)
  axes = plt.gca()
  axes.set_ylim([-0.2 , 1])
  plt.plot(x,y)
  plt.savefig(f'{folder_path}/{filename}.png')

def run_1000(num_participants, num_steals):
  out = {}
  out2 = {}
  for _ in range(1000):
    white_elephant_sim = WhiteElephantSim(num_participants, num_steals)
    white_elephant_sim.run()

    vals = white_elephant_sim.get_relative_values()
    for i in vals:
      if i not in out:
        out[i] = []
      out[i].append(vals[i])

    vals2 = white_elephant_sim.get_values()
    for i in vals2:
      if i not in out2:
        out2[i] = []
      out2[i].append(vals2[i])

  avg_return = {}
  for o in out:
    avg_return[o] = np.mean(out[o])
  avg_value = {}
  for o in out2:
    avg_value[o] = np.mean(out2[o])

  return avg_return, avg_value

def main():
  NUMBER_OF_PARTICIPANTS = 100
  MAX_STEALS = 100
  avg_return, avg_value = run_1000(NUMBER_OF_PARTICIPANTS,m)
  save_graph_return(f'{MAX_STEALS}_{NUMBER_OF_PARTICIPANTS}_avg_return', avg_return)
  save_graph_value(f'{MAX_STEALS}_{NUMBER_OF_PARTICIPANTS}_value_return', avg_value)

if __name__ == '__main__':
  main()