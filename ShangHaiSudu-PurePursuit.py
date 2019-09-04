import math
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

    reward = 1e-3
    
    rabbit = [0,0]
    pointing = [0,0]
        
    # Reward when yaw (car_orientation) is pointed to the next waypoint IN FRONT.
    
    # Find nearest waypoint coordinates
    
    rabbit = [waypoints[closest_waypoints[1]][0],waypoints[closest_waypoints[1]][1]]
    
    radius = math.hypot(x - rabbit[0], y - rabbit[1])
    
    pointing[0] = x + (radius * math.cos(heading))
    pointing[1] = y + (radius * math.sin(heading))
    
    vector_delta = math.hypot(pointing[0] - rabbit[0], pointing[1] - rabbit[1])
    
    # Max distance for pointing away will be the radius * 2
    # Min distance means we are pointing directly at the next waypoint
    # We can setup a reward that is a ratio to this max.
    
    if vector_delta == 0:
        reward += 1
    else:
        reward += ( 1 - ( vector_delta / (radius * 2)))
        
    if speed >= 6:
        reward +=0.3
    if speed >= 4:
        reward +=0.1
    if speed >= 2:
        reward +=0.01

    print('Reward {:.2f}, x: {:.2f}, y: {:.2f}, vector_delta: {:.2f}, rabbit: {}, radius: {:.2f}, pointing: {}, Params: {}'.format(reward, x, y, vector_delta, rabbit, radius, pointing, params))
    
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
          'speed': 5.67
        }   



print ('Middle Track: {}'.format(reward_function(params1)))


