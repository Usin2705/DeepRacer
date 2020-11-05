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
    # Need: distance_from_center + track_width

    # This version splits the car's distance from center to 20 markers
    # then depend on the current marker the car is in, give its corresponding
    # reward (or penalty)
    # Example:
    # distance from center: [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    # Reward list         : [1.0, 0.8, 0.6,-0.2,-0.6,-1.0]
    
    myMarker = []
    myN = 20 # split the distance from center by 20
    
    # Prepare the marker, increase by 0.05 each
    for i in range (myN):
        myMarker.append(round(0.05*i,2))

    # Prepare the positive reward for half of the markers
    myReward = []
    for i in range (int(myN/2)):
        myReward.append(0.05*(myN-i))
    
    # Adding the negative reward for the rest of the markers
    for i in range (int(myN/2)):
        myReward.append(-0.1*(i))    
        
    # Give higher reward if the car is closer to center line and vice versa
    closestValue = min(myMarker, key=lambda x:abs(x-distance_from_center/track_width))
    myMarkerIndex = [i for i,x in enumerate(myMarker) if x == closestValue][0]
    reward = myReward[myMarkerIndex]
       
    return float(reward)
