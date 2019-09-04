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

   
    # 49 waypoints
    # let's say each waypoint need 1 steps
    # you could get about 50 steps at 100 progress -> reward = 20
    # speed should be increase if you want more impact for faster fun
    if steps > 0:
        reward = (progress*10/steps) + speed/4
    else:
        reward = 0
        
    print('Reward {:.2f}, progess: {:.2f}, step: {}, speed: {}, Params: {}'
          .format(reward, progress, steps, speed, params))
        
    return float(reward)


 
params1 = {'all_wheels_on_track': True,
          'track_width': 3,
          'distance_from_center': 0.1,
          'is_left_of_center': True,
          'heading': 0,
          'progress': 10,
          'steering_angle': 0,          
          'x': 0.1,
          'y': 0.4,
          'headings': 0.14,
          'waypoints': [[0.1,0.02], [0.2,0.04]],
          'closest_waypoints': (1, 1),
          'speed': 8,
          'steps': 31
        }   



print ('Middle Track: {}'.format(reward_function(params1)))


