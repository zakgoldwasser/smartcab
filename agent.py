import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import numpy as np

global x,reward_d,Q_dict,last_state,last_action
x = 0
r_list=[]
Q_dict= {}
last_state=[]
last_action=[]


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        Q_dict= {}
        r_list=[]

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        #inputs = inputs.items()
        #print(inputs)

        # TODO: Update state
        self.state = (inputs['light'],inputs['oncoming'],self.next_waypoint)
        #print (self.state)
        
        # TODO: Select action according to your policy
        actions= (None, 'forward', 'left', 'right')
        if self.state not in Q_dict: #is state in Q_dict?
            print("not")
            Q_dict[self.state]={} #if not add it
            for a in actions:
                Q_dict[self.state][a]= 0 #sets each action as key to later give a q val
            
            action = random.choice(actions) #choose random action
            last_state.append(self.state)

        else:
            unexplored_states=[k for k,v in Q_dict[self.state].items() if v == 0]
            #print(len(unexplored_states))
            if x % 5 == 0:
                if len(unexplored_states)!=0:
                    print('un',unexplored_states)
                    action = random.choice(unexplored_states)

            #print("in")
            gamma = .8
            old_r= r_list[x-1]
            max_list = []
            #print(Q_dict[self.state])
            q_max=max(Q_dict[self.state].values())
            #print(q_max)
            max_list= [k for k,v in Q_dict[self.state].items() if v == q_max]
            #print(max_list)
            max_dir= random.choice(max_list)
            #print(max_dir)
            q_val = old_r + (gamma * q_max) #qformula
            #print(Q_dict[last_state[0]],Q_dict[self.state])
            Q_dict[last_state[0]][last_action[0]]=q_val #adds q value for state,action
            #print("post",Q_dict[self.state])
            action= max(Q_dict[self.state]) #chooses max action for that state
            del last_action[0]
            del last_state[0]
            

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        
        r_list.append(reward)
        last_state.append(self.state)
        last_action.append(action)
        global x
        x=x+1
        r_list.append(reward)
        #print(np.mean(r_list))
        #print(Q_dict)
        #print (Q_dict)

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
