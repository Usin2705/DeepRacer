# DeepRacer
AWS DeepRacer reward functions and stuffs

Local training using: https://github.com/alexschultz/deepracer-for-dummies

Some FAQ for erros: https://codelikeamother.uk/training-locally-for-aws-deepracer-and-a-udacity-challenge-with-rewards

### How to view log file in docker:
Basically, the log and the print() result are output in deepracer_robomaker:console
Because this log is contained inside docker, we need to view it inside docker.

First, we need to find the id of container (find the ID of deepracer_robomaker:console)
```
docker ps
```

Secondly, show the log and auto update with last info:
```
docker logs -f --tail 30 {ID}
```
Now you know more about docker, use this quick and easy way (it's the same thing, just skip the ID and go straight to the name)
```
docker logs -f --tail 30 robomaker
```


SIM_TRACE_LOG explain:

SIM_TRACE_LOG:EPISODE,STEP,X,Y,HEADING(RAD),STEERING(RAD),SPEED,ACTION_INDEX,REWARD,DONE(bool),IS_WHEEL_ON_TRACK(bool),PROGRESS,CLOSEST_WAYPOINTS,TRACK_LENGTH,TIME

