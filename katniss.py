from __future__ import print_function
from __future__ import division
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

def targetWall(env):
    z1 = env[0]
    z2 = env[1]
    y1 = env[2]
    y2 = env[3]
    x = env[4]
    targY = env[5]
    targZ = env[6]
    ret_str = ""
    ret_str += '<DrawCuboid x1="' + str(x) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x+1) + '" y2="' + str(y2) + '" z2="' + str(z2) + '" type="air"/>\n'
    for y in range(y1, y2):
        for z in range(z1, z2):
            ret_str += '''<DrawBlock type='stone' x="''' + str(x) + '''" y="'''+ str(y) + '''" z="''' + str(z) +'''" />
            '''
    for y in range(y1, y2):
        for z in range(z1, z2):
            if (y==targY) and (z==targZ):
                ret_str += '''<DrawItem type='apple' x="''' + str(x+1) + '''" y="'''+ str(y) + '''" z="''' + str(z) +'''" />
                '''
                continue
            ret_str += '''<DrawBlock type='stone' x="''' + str(x+1) + '''" y="'''+ str(y) + '''" z="''' + str(z) +'''" />
            '''
    return ret_str

def genXML(envDescription):
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
                  <FlatWorldGenerator forceReset="0" generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"/>
                  <DrawingDecorator>
                    ''' + targetWall(envDescription) + '''
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="3000"/>
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

def evaluateFitness(environment, motor_function):
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
        missionXML=genXML(environment)
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
        s = time.time()
        agent_y = 0
        agent_z = 0
        agent_yaw = 0
        agent_pitch = 0
        arrow_y = 0
        arrow_z = 0
        arrow_x = 0
        target_y = 0
        target_z = 0
        target_x = 0
        arrow_x = 0
        while world_state.is_mission_running:
            time.sleep(0.01)
            world_state = agent_host.getWorldState()
            for error in world_state.errors:
                print("Error:",error.text)
            shoot = 1 if (time.time() - s < 1.5) else 0
                
            #agent_host.sendCommand("pitch " + str(random.random()*2 - 1))
            agent_host.sendCommand("use " + str(shoot))

            if world_state.number_of_observations_since_last_state > 0:
                msg = world_state.observations[-1].text
                ob = json.loads(msg)
                #print(ob)
                if u'entities' in ob:
                    entities = ob["entities"]

                    for e in entities:
                        if e["name"] == "agent":
                            agent_y = e["y"]
                            agent_z = e["z"]
                            agent_yaw = e["yaw"]
                            agent_pitch = e["pitch"]
                        if e["name"] == "apple":
                            target_y = e["y"]
                            target_z = e["z"]
                            target_x = e["x"]
                        if e["name"] == "Arrow":
                            arrow_y = e["y"]
                            arrow_z = e["z"]
                            arrow_x = e["x"]
                            min_distance = math.sqrt(math.pow(arrow_y - target_y, 2) + math.pow(arrow_z - target_z, 2) + math.pow(arrow_x - target_x, 2))
                            
            agent_host.sendCommand("turn " + str(motor_function[0]))
            agent_host.sendCommand("pitch " + str(motor_function[1]))
        print("Mission ended")
        print("Distance was {0}".format(min_distance))
        return 1/min_distance
