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
step = 4
v_width = 432*2
v_height = 240*2
sensor_y = 4
sensor_x = 4
def processFrame(frame):
    sensors = []
    for y in range(0, sensor_y):
        sensors.append([])
        for x in range(0, sensor_x):
            sensors[len(sensors)-1].append(0)
    #print(len(frame))
    #print(v_height * v_width * 3)
    for i in range(0, len(frame), (step*3)+3):
        col = (frame[i], frame[i+1], frame[i+2])
        if col[0] > max(col[1], col[2])*1.1:
            vert = math.floor(i/(len(frame)/sensor_y))
            col = (i - (v_width * math.floor(i/v_width)))
            hor =  math.floor(col/(v_width/sensor_x))
            #print(vert)
            #print(hor)
            sensors[vert][hor] += 1
            #print(col)
    return [item for sublist in sensors for item in sublist]

def fake_nn(inputs):
    yaw_weights = [-1, -0.5, 0.5, 1, -1, -0.5, 0.5, 1, -1, -0.5, 0.5, 1, -1, -0.5, 0.5, 1]
    pitch_weights = [-1, -1, -1, -1, -0.5, -0.5, -0.5, -0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1]
    yaw_out = 0
    pitch_out = 0
    for i,val in enumerate(inputs):
        yaw_out += yaw_weights[i]*inputs[i]
        pitch_out += pitch_weights[i]*inputs[i]
    return [yaw_out, pitch_out]

def targetWall(z1, z2, y1, y2, x):
    ret_str = ""
    ret_str += '<DrawCuboid x1="' + str(x) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x+5) + '" y2="' + str(y2) + '" z2="' + str(z2) + '" type="air"/>\n'
    for y in range(y1, y2):
        for z in range(z1, z2):
            ret_str += '''<DrawBlock type='stone' x="''' + str(x) + '''" y="'''+ str(y) + '''" z="''' + str(z) +'''" />
            '''
    rand_y = random.randint(y1+1, y2-1)
    rand_z = random.randint(z1+1, z2-1)
    for y in range(y1, y2):
        for z in range(z1, z2):
            if (y==rand_y) and (z==rand_z):
                ret_str += '''<DrawItem type='apple' x="''' + str(x+1) + '''" y="'''+ str(y) + '''" z="''' + str(z) +'''" />
                '''
                continue
            ret_str += '''<DrawBlock type='stone' x="''' + str(x+1) + '''" y="'''+ str(y) + '''" z="''' + str(z) +'''" />
            '''
    return ret_str

def genXML():
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
                  <FlatWorldGenerator forceReset="0" generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,1;12;"/>
                  <DrawingDecorator>
                    ''' + targetWall(10, 20, 56, 65, 0) + '''
                  </DrawingDecorator>
                  <MovingTargetDecorator>
                    <ArenaBounds>
                       <min x="2" y="56" z="10"/>
                       <max x="2" y="65" z="20"/>
                    </ArenaBounds>
                    <StartPos x="2" y="60" z="11"/>
                    <Seed>1</Seed>
                    <UpdateSpeed>10</UpdateSpeed>
                    <PermeableBlocks type="redstone_block emerald_block purpur_block air"/>
                    <BlockType type="redstone_block"/>
                </MovingTargetDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="30000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>agent</Name>
                <AgentStart>
                    <Placement x="15" y="56.0" z="15" yaw="90"/>
                    <Inventory>
                        <InventoryItem slot="8" type="bow"/>
                        <InventoryItem slot="7" type="arrow" quantity="64" />
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                    <VideoProducer>
                       <Width>''' + str(v_width) + '''</Width>
                       <Height>''' + str(v_height) + '''</Height>
                     </VideoProducer>
                  <ObservationFromFullStats/>
                  <ObservationFromGrid>
                      <Grid name="floor3x3">
                        <min x="-1" y="-1" z="-1"/>
                        <max x="1" y="-1" z="1"/>
                      </Grid>
                  </ObservationFromGrid>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="1000" yrange="1000" zrange="1000" />
                </ObservationFromNearbyEntities>
                  <ContinuousMovementCommands turnSpeedDegs="20"/>
                  <InventoryCommands/>
                  <ChatCommands />
                  <AgentQuitFromTouchingBlockType>
                      <Block type="diamond_block" />
                  </AgentQuitFromTouchingBlockType>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

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
    missionXML=genXML()
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
    agent_host.sendCommand("hotbar.9 1")
    agent_host.sendCommand("hotbar.9 0")
    # Loop until mission ends:
    s = time.time()
    agent_y = 0
    agent_z = 0
    agent_yaw = 0
    agent_pitch = 0
    arrow_y = 0
    arrow_z = 0
    target_y = 0
    target_z = 0
    while world_state.is_mission_running:
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)
        #print(time.time() - s)
        #shoot = 1 if (time.time() - s < 1.5) else 0
            
        #agent_host.sendCommand("pitch " + str(random.random()*2 - 1))
        #agent_host.sendCommand("use " + str(shoot))

        while world_state.number_of_video_frames_since_last_state < 1 and world_state.is_mission_running:
            time.sleep(0.005)
            world_state = agent_host.getWorldState()
        
        if world_state.is_mission_running:
            sensors = processFrame(world_state.video_frames[0].pixels)
            print(sensors)
            if sum(sensors) > 0:
                yaw_o,pitch_o = fake_nn(sensors)
                y_sign = -1 if yaw_o < 0 else 1
                p_sign = -1 if pitch_o < 0 else 1
                yaw_o = yaw_o/sum(sensors) 
                pitch_o = pitch_o/sum(sensors)
                max_speed = 0.3
                if yaw_o < -max_speed:
                    yaw_o = -max_speed
                if yaw_o > max_speed:
                    yaw_o = max_speed            
                if pitch_o < -max_speed:
                    pitch_o = -max_speed
                if pitch_o > max_speed:
                    pitch_o = max_speed
                print(yaw_o)
                agent_host.sendCommand("turn " + str(yaw_o))
                agent_host.sendCommand("pitch " + str(pitch_o))

    print()
    print("Mission ended")
    print("Distance was {0}".format(min_distance))
    agent_host.sendCommand("chat %s" % min_distance)
    # Mission has ended.
