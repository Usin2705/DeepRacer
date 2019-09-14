import math
def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    
    # float
    # Location in meters of the vehicle center along the x axis of the simulated 
    # environment containing the track. The origin is at the lower-left corner of 
    # the simulated environment.
    x = params['x']    
    
    # float
    # Location in meters of the vehicle center along the y axis of the simulated 
    # environment containing the track. The origin is at the lower-left corner of 
    # the simulated environment.    
    y = params['y']    
    
    # heading
    # float (-180, 180]
    # Heading direction in degrees of the vehicle with respect to the x-axis 
    # of the coordinate system.
    heading = params['heading']    
    
    # float [0, 100]
    # Percentage of the track complete.
    progress = params['progress']
    
    # integer
    # Number of steps completed. One step is one (state, action, next state, reward tuple).
    steps = params['steps']
    
    # waypoints
    # List of (float, float)
    # An ordered list of milestones along the track center. Each milestone is 
    # described by a coordinate of (x, y). 
    waypoints = params['waypoints']    
    
    # closest_waypoints
    # (integer, integer)
    # The zero-based indices of the two neighboring waypoints closest to the 
    # vehicle's current position of (x, y). The distance is measured by the 
    # Euclidean distance from the center of the vehicle.
    closest_waypoints = params['closest_waypoints']    
    
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

    reward = 1e-4
    rewardLn = 1e-4
    
    # As distance from center often stay around 0.5 of track_width.
    # Any normDistance > 0.5 would indicate it is almost offtrack
    normDistance = distance_from_center/track_width
    
    # this should give car full reward, the distance should be large enough
    # Sometime car need to go out of the middle (sharp turn), and it's ok, we should not
    # punish it
    BEST_DISTANCE = 0.1
    OK_DISTANCE = 0.2 
    AVG_DISTANCE = 0.35	
    BAD_DISTANCE = 0.5  # The rest is impossible to save
    
    
    strPos = "UNK"
    
    

    if (steps>=3):
        reward = 5.2 + 4*math.log(progress/steps)
        rewardLn = 5.2 + 4*math.log(progress/steps)
    
    if (normDistance<=BEST_DISTANCE):
        strPos = "BST"
        reward += 0.6        
        
    elif(normDistance<=OK_DISTANCE):
        strPos = "OKE"
        reward +=0.48       
    
    elif (normDistance<=AVG_DISTANCE):
        strPos = "AVG"
        reward += 0.24

    elif (normDistance<=BAD_DISTANCE):
        strPos = "BAD"
        reward += 0.12

    else:
        strPos = "IMM"
        reward += 1e-4
        
    if (reward <= 0):
        reward = 1e-4
        
    carString=('REW: {:7.4f}, RLN {:.2f} POS: {}, TURN: {:3.0f}, SPE: {:.2f}, IS_LEFT {}, NORMDIST: {:.2f}, DISTANCE: {:.2f}'
               ', TRACK_WIDTH: {:.2f}, STEP: {}, PRO: {:2f}'.format(reward, rewardLn, strPos, 
                steering_angle, speed, is_left_of_center, normDistance, distance_from_center, track_width, steps, progress))

    print(carString)        
    return float(reward)


 
offtrack = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 1.6,
          'is_left_of_center': True,
          'heading': 0,
          'progress': 7.2,
          'steering_angle': -20,
          'speed': 5.33,
          'x': 3.12,
          'y': 1.15,
          'steps': 12,
          'waypoints': [1.21, 0.26],
          'closest_waypoints': 2
        }       

params2 = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 0.5,
          'is_left_of_center': False,
          'heading': 0,
          'progress': 1.2,
          'steering_angle': 10,
          'speed': 2.67,
          'x': 3.12,
          'y': 1.15,
          'steps': 5,
          'waypoints': [1.21, 0.26],
          'closest_waypoints': 2
        }  

params3 = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 0.3,
          'is_left_of_center': True,
          'heading': 0,
          'progress': 10,
          'steering_angle': -10,
          'speed': 8,
          'x': 3.12,
          'y': 1.15,
          'steps': 12,
          'waypoints': [1.21, 0.26],
          'closest_waypoints': 2
        }  

params4 = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 0.1,
          'is_left_of_center': True,
          'heading': 0,
          'progress': 10,
          'steering_angle': 0,
          'speed': 5.33,
          'x': 3.12,
          'y': 1.15,
          'steps': 12,
          'waypoints': [1.21, 0.26],
          'closest_waypoints': 2
        }   

params5 = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 1.2,
          'is_left_of_center': True,
          'heading': 0,
          'progress': 10,
          'steering_angle': -30,
          'speed': 5.33,
          'x': 3.12,
          'y': 1.15,
          'steps': 12,
          'waypoints': [1.21, 0.26],
          'closest_waypoints': 2
        }   

params6 = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 1.2,
          'is_left_of_center': False,
          'heading': 0,
          'progress': 10,
          'steering_angle': 30,
          'speed': 5.33,
          'x': 3.12,
          'y': 1.15,
          'steps': 12,
          'waypoints': [1.21, 0.26],
          'closest_waypoints': 2
        }   


params7 = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 1.4,
          'is_left_of_center': True,
          'heading': 0,
          'progress': 10,
          'steering_angle': -30,
          'speed': 5.33,
          'x': 3.12,
          'y': 1.15,
          'steps': 12,
          'waypoints': [1.21, 0.26],
          'closest_waypoints': 2
        }   

params8 = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 1.4,
          'is_left_of_center': False,
          'heading': 0,
          'progress': 10,
          'steering_angle': 30,
          'speed': 5.33,
          'x': 3.12,
          'y': 1.15,
          'steps': 12,
          'waypoints': [1.21, 0.26],
          'closest_waypoints': 2
        }   




print ('Off Track, left, 0 steering: {}'.format(reward_function(offtrack)))
print ('near middle Track, right, 10 steering: {}'.format(reward_function(params2)))
print ('nearer middle Track, left, -10 steering: {}'.format(reward_function(params3)))
print ('Middle Track: {}'.format(reward_function(params4)))
print ('Turn sharp left when near left offtrack: {}'.format(reward_function(params5)))
print ('Turn sharp right when near right offtrack: {}'.format(reward_function(params6)))
print ('Turn sharp left when almost left offtrack: {}'.format(reward_function(params7)))
print ('Turn sharp right when almost right offtrack: {}'.format(reward_function(params8)))
