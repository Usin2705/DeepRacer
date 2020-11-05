import math
def reward_function(params):
    '''
    Reward function for AWS deeprace
    
    Parameters
    ----------
    params : py:class:`dict`
        The dictionary contain all parameters for DeepRacer

    Returns
    -------
    reward : py:class:`float`
        The reward from DeepRacer's action, must be float otherwise AWS won't
        accept it        
    '''
    
    # Read input parameters. Copy from the InputParamater.py        

    reward = 1e-4
    rewardLn = 1e-4
    
    # Normalize the car distance from center so we can use it in different tracks
    # As distance from center often stay around 0(center) to 0.5 of track_width.
    # any normDistance > 0.5 would indicate it is almost offtrack
    normDistance = distance_from_center/track_width
    
    # Distrance from center at 0 mean the car stay at the center, this should 
    # give car full reward, the distance should be large enough to allow the
    # car to make sharpe turn (Sometime car need to go out of the middle to make
    # a sharp turn). So car also receive reward even if it went out of middle
    BEST_DISTANCE = 0.1
    OK_DISTANCE = 0.2 
    AVG_DISTANCE = 0.35	
    BAD_DISTANCE = 0.5  # The rest is impossible to save, we call its IMM
    
    strPos = "UNK"
       
    # Give reward based on progress & steps
    if (steps>=3):
        reward = 5.2 + 4*math.log(progress/steps)
        rewardLn = 5.2 + 4*math.log(progress/steps)
    
    # Adjust reward for position
    if (normDistance<=BEST_DISTANCE):
        strPos = "BST"
        reward += 0.8        
        
    elif(normDistance<=OK_DISTANCE):
        strPos = "OKE"
        reward +=0.64       
    
    elif (normDistance<=AVG_DISTANCE):
        strPos = "AVG"
        reward += 0.32

    elif (normDistance<=BAD_DISTANCE):
        strPos = "BAD"
        reward += 0.16

    else:
        strPos = "IMM"
        reward += 1e-4
        
    #Sometime, the reward are negative (due to the ln reward function)
    if (reward <= 0):
        reward = 1e-4        
    
    # Print the parameter out to console (so we can see it in local training)
    carString=('REW: {:7.4f}, RLN {:.2f} POS: {}, TURN: {:3.0f}, SPE: {:.2f}, '
               'IS_LEFT {}, NORMDIST: {:.2f}, DISTANCE: {:.2f}', '
               'TRACK_WIDTH: {:.2f}'.format(reward, rewardLn, strPos, 
                steering_angle, speed, is_left_of_center, normDistance, 
                distance_from_center, track_width))
    print(carString)        
    
    return float(reward)
