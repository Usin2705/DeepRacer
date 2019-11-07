# -*- coding: utf-8 -*-
"""
AWS DeepRacer reward function

@author: Usin
"""


# https://github.com/breadcentric/aws-deepracer-workshops/blob/enhance-log-analysis/log-analysis/reward/reward_sample.py
class MyCar:
    def __init__ (self):
        self.previous_steps = None
        self.pre_progress = 0
        self.pre_progress2 = 0        
   
    def reward_function(self, params):
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
        
        # Normalize the car distance from center so we can use it in different tracks
        # As distance from center often stay around 0(center) to 0.5 of track_width.
        # any normDistance > 0.5 would indicate it is almost offtrack
        normDistance = distance_from_center/track_width     
        
        # Set the minimum step that we will reward the car for high speed
        # As the begining, the higher the speed (throttle) the better, and 
        # there's almost no problem when car run max speed as start, so we
        # just reward car if they start with higher speed
        MINIMUM_SPEEDING_STEPS = 6    
        if (steps <= MINIMUM_SPEEDING_STEPS) and (speed>= 8.5):
            reward = 1
        else:
            reward = 1e-4
    
        # We use two previous progress parameter, so the minimum step the car
        # must run before we can calculate the reward is 3
        # This will give reward depend on the car's progress increase speed, 
        # so if car increase progress faster, it will get higher reward.
        # In other words, the faster you reach the finishing line, the higher
        # reward you'll get
        if (steps>MINIMUM_SPEEDING_STEPS):
            reward = ((progress- self.pre_progress)*2)**2 + \
                     ((progress- self.pre_progress2))**2
            
        # Sometime in local training, car teleport to random location, this 
        # will lead to a huge progress reward (from 10% progress jumped to 20%
        # progress) and therefore disrupts our model. Therefore we need this 
        # to remove the teleport problem
        if ((progress - self.pre_progress)>=5) or ((progress - self.pre_progress2)>=5):
            reward = 1e-4
            
        # Avoid negative reward
        if (reward <= 0):
            reward = 1e-4
        
        # Print the parameter out to console (so we can see it in local training)                
        carString=('REW: {:3.1f}, PRO: {:5.2f}, PRE_PRO: {:5.2f}, '
                   'PRE_PRO2: {:5.2f}, TURN:{:5.1f}, SPE: {:3.1f}, '
                   'IS_LEFT {}, NORMDIST: {:.2f}, DISTANCE: {:.2f}, '
                   ' TRACK_WIDTH: {:.2f}'.format(reward, progress, 
                   self.pre_progress, self.pre_progress2, steering_angle, 
                   speed, is_left_of_center, normDistance, 
                   distance_from_center, track_width))
        print(carString)        
        
        self.pre_progress2 = self.pre_progress
        self.pre_progress = progress        
        self.previous_steps = steps
        return float(reward)        

myCarObject = MyCar()
        
def reward_function(params):
    '''
    Reward function for AWS deeprace. This will pass params to a Python object
    so we can store the previous params. (Our reward will depend on the current
    params and also past params)
    
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
    
    return myCarObject.reward_function(params)    


