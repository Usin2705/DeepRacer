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

show the log and auto update with last info:
```
docker logs -f --tail 10 {ID}
```
SIM_TRACE_LOG explain:

SIM_TRACE_LOG:EPISODE,STEP,2.5332,-0.9551,-1.6821,0.17,8.00,14,1.0000,False,True,13.8450,15,22.92,1567602913.1932492

