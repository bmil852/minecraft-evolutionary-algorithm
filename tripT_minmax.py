from __future__ import print_function
from __future__ import division
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #5: Observations

from builtins import range
from past.utils import old_div
import MalmoPython
import os
import sys
import time
import json
import random
import math
if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

class MinMaxAgent:
    def __init__(self, state_rewards, p_num):
        self.state_rewards = state_rewards
        self.p_num = p_num
    
    def act(self, state, r, c):
        print(state)
        next_op = self.state_rewards[json.dumps(state)]
        print(next_op)
        next_state = json.loads(next_op[3][2])
        print(next_state)
        return next_state

class Agent:
    def __init__(self, p_num):
        self.p_num = p_num
    def act(self, state, r, c):
        print("agent {0}".format(self.p_num))
        possible_actions = []
        for s_y in range(0, r):
            for s_x in range(0, c):
                s = state[s_y * c + s_x]
                if s == -1:
                    state_copy = state[:]
                    state_copy[s_y * c + s_x] = self.p_num
                    one_turn_reward = 0
                    for delta in [[0, 1, 0, -1], [1, 1, -1, -1], [1, 0, -1, 0], [-1, 1, 1, -1], [0, 1, 0, 2], [1, 1, 2, 2], [1, 0, 2, 0], [1, -1, 2, -2], [0, -1, 0, -2], [-1, -1, -2, -2], [-1, 0, -2, 0], [-1, 1, -2, 2]]:
                            along_delta = []
                            for l in range(0, 2):
                                b1_c = s_x + delta[0 + l*2]
                                b1_r = s_y + delta[1 + l*2]
                                print("check {0},{1}".format(b1_c, b1_r))
                                if(b1_c >= c or b1_c < 0 or b1_r >= r or b1_r < 0):
                                    print('none')
                                    along_delta.append(None)
                                else:
                                    along_delta.append(state[b1_r * c + b1_c])
                            # if along_delta[0] == along_delta[1] and along_delta[0] != -1 and along_delta[0] != None:
                            #     one_turn_reward += 100
                            # if along_delta[0] == along_delta[1] and along_delta[0] == -1 and along_delta[0] != None:
                            #     one_turn_reward += 2
                            # if along_delta[0] != along_delta[1] and (along_delta[0] == -1 or along_delta[1] == -1):
                            #     if(along_delta[0] == self.p_num or along_delta[1] == self.p_num):
                            #         one_turn_reward += 3
                            #     else:
                            #         one_turn_reward += 1
                            
                            num_empty = 0 
                            num_same = 0
                            num_other = {}
                            for i in along_delta:
                                if i == -1:
                                    num_empty += 1
                                elif i == self.p_num:
                                    num_same += 1
                                elif i != None:
                                    if i not in num_other:
                                        num_other[i] = 0
                                    num_other[i] += 1
                            print(delta)
                            print(along_delta)
                            
                            print(num_empty)
                            print(num_same)
                            print(num_other)
                            if num_empty == 2:
                                one_turn_reward += 1
                            if num_same == 2:
                                one_turn_reward += 100
                            if num_other != {} and max(num_other.values()) > 1:
                                one_turn_reward += 100
                            if num_empty == 1 and num_same == 1:
                                one_turn_reward += 1
                            if num_empty == 1 and num_other != {}:
                                one_turn_reward += 1
                    print([state_copy, one_turn_reward])
                    possible_actions.append([state_copy, one_turn_reward])
        max_reward = max(possible_actions, key= lambda item: item[1])[1]
        potential_actions = [ p for p in possible_actions if p[1] == max_reward]
        print(possible_actions)
        print(potential_actions)
        choice = potential_actions[math.floor(random.random()*len(potential_actions))][0]
        print(choice)
        return json.dumps(choice)
def genXML(r, c):
    z1 = str(14 - math.floor(c/2))
    z2 = str(14 + math.floor(c/2))
    x1 = str(16 )
    x2 = str(16 + r-1)
    #line = '<DrawCuboid x1="' + x1 + '" y1="3" z1="' + z1 + '" x2="' + x2 +" y2="4" z2="''' + z2 + '''" type="air"/>

    return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
            <ServerSection>
              <ServerInitialConditions>
                <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
              </ServerInitialConditions>
              <ServerHandlers>
                  <FlatWorldGenerator forceReset="0" />
                  <DrawingDecorator>
                    <DrawCuboid x1="''' + x1 + '''" y1="3" z1="''' + z1 + '''" x2="''' + x2 +'''" y2="4" z2="''' + z2 + '''" type="air"/>
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="1000000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>agent</Name>
                <AgentStart>
                    <Placement x="16" y="4.0" z="15" yaw="-90" pitch="60"/>
                    <Inventory>
                        <InventoryItem slot="0" type="stone" quantity="64"/>
                        <InventoryItem slot="1" type="glowstone" quantity="64" />
                        <InventoryItem slot="2" type="log" quantity="64" />
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ObservationFromRay/>
                  <ObservationFromGrid>
                      <Grid name="floor3x3">
                        <min x="-1" y="-1" z="-1"/>
                        <max x="1" y="-1" z="1"/>
                      </Grid>
                  </ObservationFromGrid>
                  <ContinuousMovementCommands turnSpeedDegs="20"/>
                  <InventoryCommands/>
                  <ChatCommands />
                  <AgentQuitFromTouchingBlockType>
                      <Block type="diamond_block" />
                  </AgentQuitFromTouchingBlockType>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''
# def is_winning(state, player, r, c):
#     winning = False
#     for s_y in range(0, r):
#         for s_x in range(0, c):
#             if state[s_y * c + s_x] == player:
#                 sum_h = 1
#                 for x in range(s_x+1, s_x + 3):
#                     if x >= c:
#                         continue
#                     if state[s_y * c + x] == player:
#                         sum_h += 1
#                 if sum_h >= 3:
#                     return True
#                 sum_v = 1
#                 for y in range(s_y + 1, s_y + 3):
#                     if y >= r:
#                         continue
#                     if state[y * c + s_x] == player:
#                         sum_v += 1
#                 if sum_v >= 3:
#                     return True
#                 sum_d = 1
#                 for d in range(1, 3):
#                     if s_x + d >= c or s_y+d >= r:
#                         continue
#                     if state[(s_y + d) * c + (s_x + d)] == player:
#                         sum_d += 1
#                 if sum_d >= 3:
#                     return True
#                 sum_d = 1
#                 for d in range(1, 3):
#                     if s_x - d < 0 or s_y+d >= r:
#                         continue
#                     if state[(s_y + d) * c + (s_x - d)] == player:
#                         sum_d += 1
#                 if sum_d >= 3:
#                     return True
#     return False
def is_winning(state, player, r, c):
    for s_y in range(0, r):
        for s_x in range(0, c):
            if state[s_y * c + s_x] != player:
                continue
            one_turn_reward = 0
            for delta in [[0, 1, 0, -1], [1, 1, -1, -1], [1, 0, -1, 0], [-1, 1, 1, -1], [0, 1, 0, 2], [1, 1, 2, 2], [1, 0, 2, 0], [1, -1, 2, -2], [0, -1, 0, -2], [-1, -1, -2, -2], [-1, 0, -2, 0], [-1, 1, -2, 2]]:
                    along_delta = []
                    for l in range(0, 2):
                        b1_c = s_x + delta[0 + l*2]
                        b1_r = s_y + delta[1 + l*2]
                        #print("check {0},{1}".format(b1_c, b1_r))
                        if(b1_c >= c or b1_c < 0 or b1_r >= r or b1_r < 0):
                            #print('none')
                            along_delta.append(None)
                        else:
                            #print(state[b1_r * c + b1_c])
                            along_delta.append(state[b1_r * c + b1_c])
                    # if along_delta[0] == along_delta[1] and along_delta[0] != -1 and along_delta[0] != None:
                    #     one_turn_reward += 100
                    # if along_delta[0] == along_delta[1] and along_delta[0] == -1 and along_delta[0] != None:
                    #     one_turn_reward += 2
                    # if along_delta[0] != along_delta[1] and (along_delta[0] == -1 or along_delta[1] == -1):
                    #     if(along_delta[0] == player or along_delta[1] == player):
                    #         one_turn_reward += 3
                    #     else:
                    #         one_turn_reward += 1
                    
                    num_empty = 0 
                    num_same = 0
                    num_diff = 0
                    for i in along_delta:
                        if i == -1:
                            num_empty += 1
                        elif i == player:
                            num_same += 1
                        elif i != None:
                            num_diff += 1
                    if num_same == 2:
                        return True
    return False
def is_reflect(states, state_inp, r, c):
    print('looking')
    o_s = state_inp[:]
    m_s = [[]]
    c_counter = 0
    r_counter = 0
    for s in state_inp:
        m_s[r_counter].append(s)
        c_counter += 1
        if c_counter == c:
            c_counter = 0
            r_counter += 1
            if r_counter < r:
                m_s.append([])
    state = m_s


    if json.dumps([item for sublist in state for item in sublist]) in states:
        return True
    for i in range(0, 4):
        state = list(zip(*state[::-1]))
        if json.dumps([item for sublist in state for item in sublist]) in states:
            return True
    h_ref = []
    for r_c in range(0, r):
        h_ref.append(state[r_c][::-1])
    if json.dumps([item for sublist in h_ref for item in sublist]) in states:
        return True
    v_ref = []
    s_t = list(zip(*state))
    for r_c in range(0, r):
        v_ref.append(s_t[r_c][::-1])
    v_ref =list(zip(*v_ref))
    if json.dumps([item for sublist in v_ref for item in sublist]) in states:
        return True
    return False
def minMaxGame(r, c, p):
    initial_state = [-1 for i in range(0, r*c)]
    states = {}
    stack = []
    stack.append([initial_state, 0, 0, [], []])
    while len(stack) > 0:
        #print(stack)
        print(len(states))
        current_state = stack[len(stack) - 1]
        checked_all_next = True
        for i in range(current_state[1], r*c):
            if current_state[0][i] == -1:
                current_state[1] = i+1
                checked_all_next = False
                break

        if not checked_all_next:
            new_state = current_state[0][:]
            # if is_reflect(states, new_state, r, c):
            #     #print('is')
            #     continue
            player = current_state[2]%p
            new_state[i] = player
            winning = is_winning(new_state, player, r, c)
            if winning:
                current_state[4].append((player, current_state[2] + 1, json.dumps(new_state)))
                current_state[3] =(player, current_state[2] + 1, json.dumps(new_state))
                stack.pop()
            else:
                # if is_reflect(states, new_state, r, c):
                #     #print('is')
                #     continue
                stack.append([new_state, 0, player + 1, [], []])
        else:
            #print('else')
            if current_state[1] == 0 and len(current_state[4]) == 0:
                s = json.dumps(current_state[0])
                current_state[3] = (-1, current_state[1], s)
                states[json.dumps(current_state[0])] = current_state
                stack.pop()
                if(len(stack) == 0):
                    break
                current_state = stack[len(stack) - 1]
                current_state[4].append((-1, current_state[1], s))
            else:
                player = current_state[2]%p
                min_win_length = None
                min_state = None
                for path_ends in current_state[4]:
                    if path_ends[0] == player:
                        if min_win_length == None or min_win_length > path_ends[1]:
                            min_win_length = path_ends[1]
                            min_state = path_ends[2]
                if min_win_length != None:
                    s = json.dumps(current_state[0])
                    s_p = json.dumps(min_state)
                    current_state[3] = (player, min_win_length, s_p)
                    states[s] = current_state
                    stack.pop()
                    if(len(stack) == 0):
                        break
                    current_state = stack[len(stack) - 1]
                    current_state[4].append((player, min_win_length, s))
                else:
                    possible_ties = []
                    for path_ends in current_state[4]:
                        if path_ends[0] == -1:
                            if min_win_length == None or min_win_length > path_ends[1]:
                                min_win_length = path_ends[1]
                                min_state = path_ends[2]
                    
                    if min_win_length != None:
                        possible_ties = [x for x in current_state[4] if x[0] == -1]
                        min_state = possible_ties[math.floor(random.random()*len(possible_ties))][2]
                        s = json.dumps(current_state[0])
                        s_p = json.dumps(min_state)
                        current_state[3] = (-1, min_win_length, s_p)
                        states[s] = current_state
                        stack.pop()
                        if(len(stack) == 0):
                            break
                        current_state = stack[len(stack) - 1]
                        current_state[4].append((-1, min_win_length, s))
                    else:
                        min_player = None
                        for path_ends in current_state[4]:
                            
                                if min_win_length == None or min_win_length < path_ends[1]:
                                    min_win_length = path_ends[1]
                                    min_player = path_ends[0]
                                    min_state = path_ends[2]
                        if min_win_length != None:
                            s = json.dumps(current_state[0])
                            s_p = json.dumps(min_state)
                            current_state[3] = (min_player, min_win_length, s_p)
                            states[s] = current_state
                            stack.pop()
                            if(len(stack) == 0):
                                break
                            current_state = stack[len(stack) - 1]
                            current_state[4].append((min_player, min_win_length, s))
                        else:
                            stack.pop()
    return states
# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

for its in range(0, 1000):
    r = 3
    c = 3
    grid_left = 14 - math.floor(c/2)
    grid_bottom = 16
    missionXML=genXML(r, c)
    my_mission = MalmoPython.MissionSpec(missionXML, True)
    my_mission_record = MalmoPython.MissionRecordSpec()

    # Attempt to start a mission:
    max_retries = 3
    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_mission_record )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission:",e)
                exit(1)
            else:
                time.sleep(2)

    # Loop until mission starts:
    print("Waiting for the mission to start ", end=' ')
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        print(".", end="")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)

    print()
    print("Mission running ", end=' ')


    min_distance = 1000
    agent_host.sendCommand("hotbar.1 1")
    agent_host.sendCommand("hotbar.1 0")
    # Loop until mission ends:

    def angvel( target, current, scale):
        '''Use sigmoid function to choose a delta that will help smoothly steer from current angle to target angle.'''
        delta = target - current
        while delta < -180:
            delta += 360
        while delta > 180:
            delta -= 360
        return (old_div(2.0, (1.0 + math.exp(old_div(-delta,scale))))) - 1.0

    def pointTo(ob, target_pitch, target_yaw, threshold):
        '''Steer towards the target pitch/yaw, return True when within the given tolerance threshold.'''
        pitch = ob.get(u'Pitch', 0)
        yaw = ob.get(u'Yaw', 0)
        delta_yaw = angvel(target_yaw, yaw, 20.0)
        delta_pitch = angvel(target_pitch, pitch, 30.0)
        agent_host.sendCommand("turn " + str(delta_yaw))    
        agent_host.sendCommand("pitch " + str(delta_pitch))
        if abs(pitch-target_pitch) + abs(yaw-target_yaw) < threshold:
            agent_host.sendCommand("turn 0")
            agent_host.sendCommand("pitch 0")
            return True
        return False
    def lookAtBlock(target, ob):
        if u'LineOfSight' not in ob:
            return
        xpos = ob.get(u'XPos', 0)
        zpos = ob.get(u'ZPos', 0)
        if zpos < target[0]:
            agent_host.sendCommand("strafe " + str(min(abs(zpos - target[0]), 1)))
        elif zpos > target[0]:
            agent_host.sendCommand("strafe " + str(-1 * min(abs(zpos - target[0]), 1)))
        los = ob[u'LineOfSight']
        los_x = float(los["x"])
        los_y = float(los["y"])
        los_z = float(los["z"])
        print(abs(los_x - target[1]))
        if False:
            t_x = target[1] + 1.5
        else:
            t_x = target[1] + 0.8
        if los_x < t_x:
            agent_host.sendCommand("pitch " + str( -1 * min(abs(los_x - t_x), 1)))
        elif los_x > t_x:
            agent_host.sendCommand("pitch " + str( 1 * min(abs(los_x - t_x), 1)))
        looking_at_target = False
        if los_y < 4:
            if los_z > target[0] - 0.5 and los_z < target[0] + 0.5:
                print('z good')
                if los_x > target[1] and los_x < target[1] + 1:
                    print('x good')
                    looking_at_target = True
            if abs(los_x  - (target[1] + 1)) < 0.1 and los_y > 3:
                looking_at_target = True
        return looking_at_target

    targets = []
    # Source grid:
    # height = 0.625  # Height from top of block (player's eyes are positioned at height of 1.625 blocks from the ground.)
    # direction = 1.0
    # for z in range(3, 0, -1):
    #     for x in range(-(old_div(3,2)),(old_div(3,2))+1):
    #         yaw = direction * x * math.atan(old_div(1.0,z)) * 180.0/math.pi
    #         distance = math.sqrt(x*x + z*z)
    #         pitch = math.atan(old_div(height,distance)) * 180.0/math.pi
    #         targets.append((pitch,yaw))
    #     direction *= -1.0
    num_player = 2
    states = minMaxGame(r, c, num_player)
    a0 = MinMaxAgent(states, 0)
    a1 = MinMaxAgent(states, 1)
    #a0 = Agent(0)
    #a1 = Agent(1)
    #a2 = Agent(2)
    #agents = [a0, a1, a2]
    agents = [a0, a1]
    state = [-1 for i in range(0, r*c)]
    done = False
    player = 0


    target = (math.floor(random.random()*c) + grid_left + 0.5, math.floor(random.random()*r) + grid_bottom)
    #print(target)
    placed = False
    done = False
    while world_state.is_mission_running and not done:
        player = player%num_player
        new_state = json.loads(agents[player].act(state, r, c))
        #print(new_state)
        diff_i = 0
        for i in range(0, len(state)):
            if state[i] != new_state[i]:
                diff_i = i
                break
        diff_r = math.floor(diff_i / c)
        diff_c = diff_i - (diff_r * c)

        extra = 0
        if diff_r == 3:
            extra = 1
        target = (diff_c + grid_left + 0.5, diff_r + grid_bottom + extra)
        while not placed and world_state.is_mission_running:
            print(".", end="")
            time.sleep(0.001)
            world_state = agent_host.getWorldState()
            for error in world_state.errors:
                print("Error:",error.text)
            
            if world_state.number_of_observations_since_last_state > 0:
                msg = world_state.observations[-1].text
                ob = json.loads(msg)
                #print(ob)

                print(target)
                # if abs(zpos - target[0]) < 0.2:
                #      agent_host.sendCommand("strafe 0")
                looking = lookAtBlock(target, ob)
                if looking and not placed:
                    agent_host.sendCommand("use 1")
                    time.sleep(0.1)
                    placed = True
                else:
                    agent_host.sendCommand("use 0")
                if u'entities' in ob:
                    entities = ob["entities"]
        agent_host.sendCommand("use 0")
        agent_host.sendCommand("strafe 0")
        agent_host.sendCommand("pitch 0")
        state = new_state
        print(state)
        if is_winning(state, player, r, c):
            done = True
            print("{0} won!".format(player))
        if all([x != -1 for x in state]):
            done = True
            print('tie')
        player += 1
        player = player % num_player
        agent_host.sendCommand("hotbar.{0} 1".format(player + 1))
        agent_host.sendCommand("hotbar.{0} 0".format(player + 1))
        placed = False
        time.sleep(0.5)
        #target = (math.floor(random.random()*c) + grid_left + 0.5, math.floor(random.random()*r) + grid_bottom)
        
    agent_host.sendCommand("use 0")
    agent_host.sendCommand("strafe 0")
    agent_host.sendCommand("pitch 0")
    print("Mission ended")
    # Mission has ended.
