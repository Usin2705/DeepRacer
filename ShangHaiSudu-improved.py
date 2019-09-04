'''
def params(para):
    if para=='all_wheels_on_track':
        return True
    elif para=='track_width':
        return 3
    elif para=='distance_from_center':
        return 1.5
    elif para=='is_left_of_center':
        return True
    elif para=='heading':
        return 0
    elif para=='progress':
        return 10
    elif para=='steering_angle':
        return 0
'''

def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    
    # x
    # float
    # Location in meters of the vehicle center along the x axis of the simulated 
    # environment containing the track. The origin is at the lower-left corner of 
    # the simulated environment.
    
    # y
    # float
    # Location in meters of the vehicle center along the y axis of the simulated 
    # environment containing the track. The origin is at the lower-left corner of 
    # the simulated environment.    
    
    # heading
    # float (-180, 180]
    # Heading direction in degrees of the vehicle with respect to the x-axis 
    # of the coordinate system.
    #heading = params['heading']    
    
    # progress
    # float [0, 100]
    # Percentage of the track complete.
    # progress = params['progress']
    
    # steps
    # integer
    # Number of steps completed. One step is one (state, action, next state, reward tuple).
    
    # waypoints
    # List of (float, float)
    # An ordered list of milestones along the track center. Each milestone is 
    # described by a coordinate of (x, y). 
    
    # closest_waypoints
    # (integer, integer)
    # The zero-based indices of the two neighboring waypoints closest to the 
    # vehicle's current position of (x, y). The distance is measured by the 
    # Euclidean distance from the center of the vehicle.
    
    # A boolean flag to indicate if the vehicle is on-track or off-track. 
    # The vehicle is off-track (False) if all of its wheels are outside of the 
    # track borders. It's on-track (True) if any of the wheels is inside the two track borders.
    all_wheels_on_track = params['all_wheels_on_track']    
        
     # float [-30, 30]
     # Steering angle, in degrees, of the front wheels from the center line of 
     # the vehicle. The negative sign (-) means steering to the right and the positive 
     # (+) sign means steering to the left.     
    steering_angle = params['steering_angle']
    
    # boolean
    # A Boolean flag to indicate if the vehicle is on the left side to the track 
    # center (True) or on the right side (False).
    is_left_of_center = params['is_left_of_center']
    
    # float
    # Track width in meters.
    track_width = params['track_width']
    
    
    # float [0.0, 8.0]
    # The observed speed of the vehicle, in meters per second (m/s).
    speed = params['speed']    
    
    # float [0, ~track_width/2]
    # Distance from the center of the track, in unit meters. The observable 
    # maximum displacement occurs when any of the agent's wheels is outside a 
    # track border and, depending on the width of the track border, can be slightly 
    # smaller or larger than half of track_width.
    distance_from_center = params['distance_from_center']

    myMarker = []
    myN = 20
    for i in range (myN):
        myMarker.append(round(0.05*i,2))

    myReward = []
    for i in range (int(myN/2)):
        myReward.append(0.05*(myN-i))
    
    for i in range (int(myN/2)):
        myReward.append(-0.1*(i))    
    
    # Give higher reward if the car is closer to center line and vice versa
    closestValue = min(myMarker, key=lambda x:abs(x-distance_from_center/track_width))
    myMarkerIndex = [i for i,x in enumerate(myMarker) if x == closestValue][0]
    reward = myReward[myMarkerIndex]
       
    return float(reward)


 
params1 = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 2.8,
          'is_left_of_center': True,
          'heading': 0,
          'progress': 10,
          'steering_angle': 0,
          'speed': 5.33
        }       

params2 = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 2,
          'is_left_of_center': True,
          'heading': 0,
          'progress': 10,
          'steering_angle': 0,
          'speed': 2.67
        }  

params3 = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 0.5,
          'is_left_of_center': True,
          'heading': 0,
          'progress': 10,
          'steering_angle': 0,
          'speed': 8
        }  

params4 = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 0.1,
          'is_left_of_center': True,
          'heading': 0,
          'progress': 10,
          'steering_angle': 0,
          'speed': 5.33
        }   




print ('OFF Track: {}'.format(reward_function(params1)))
print ('near middle Track: {}'.format(reward_function(params2)))
print ('nearer middle Track: {}'.format(reward_function(params3)))
print ('Middle Track: {}'.format(reward_function(params4)))


