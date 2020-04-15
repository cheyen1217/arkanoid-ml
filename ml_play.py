"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)
import random

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()
    tem=[0]*2
    tem[0]=-1
    tem[1]=-1
    slope=-1
    x=-1
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
       
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        else:
            
               
            
             
            #if (tem[0]==0 or tem[0]==195) and (scene_info.ball[1]>tem[1]):
            if (scene_info.ball[0]-tem[0])!=0 :          
                slope=(scene_info.ball[1]-tem[1])/(scene_info.ball[0]-tem[0])    
            if slope!=0:
                x=(400-scene_info.ball[1])/slope +scene_info.ball[0]
            elif (scene_info.ball[1]<tem[1]):
                x = 100
            
            while x<0 or x>195 :
                if x>195:
                    x = 390-x
                elif x<0 :
                    x = -x      
            
            
            kkk = random.randint(0,1)
            if kkk == 0:
                x = float(x)
                x += 2.25
            else:
                x = float(x)
                x -= 2.25
        
            if scene_info.platform[0] >x-20:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            if scene_info.platform[0] <x-20:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)

            
                      
        
        tem[0]=scene_info.ball[0]#暫存球的位置
        tem[1]=scene_info.ball[1]       
                  
                
           
