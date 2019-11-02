# DeepRacer
AWS DeepRacer reward functions and stuffs


# Models explanation
Model stored in this repo are formated this way: xx-ModelName-yy.yyy-Model_Action_Space


xx: ranking of model, the higher the better in actual AWS virtual race

ModelName: The name of model

yy.yyy: Actual shorted completed time in AWS virtual race sumission

Model_Action_Space: Some models come with their specific action space, as they require that action space to be able to has good performance

All model require variables from [InputParameter.py](https://github.com/Usin2705/DeepRacer/blob/master/InputParameter.py). That file contains all possible variable come from DeepRacer. You need to copied all necessary parameter from it to your reward function. InputParameter.py also contains faked params to test out the model and make sure it work.

## 01 [Simple](https://github.com/Usin2705/DeepRacer/blob/master/01-Simple-17.505.py) (17.505s in Shanghai Sudu):
<img src="https://github.com/Usin2705/DeepRacer/blob/master/Leaderboard-virtual-shanghai-sudo-circuit-2019-17.505.jpg">

Just as the title say, very simple model. This model was based on AWS's example model. However, instead of split the car position into 4 (0.1, 0.25, 0.5, and the rest of track will), I split it into 20 markers. I give the first half positive reward (the smaller the different the higher the reward), and the 11~20 negative reward (should not do it). I was in a hurry because I joined the race too late, around 20 August.

Also at that moment I don't have enough time to set up a local training, and don't know how to perform the log analysis. So I have no idea about the car's movement (what a pity). Due to budget reason I already delete the S3 bucket so the record is lost forever :(

## 02 [Improved-Ln](https://github.com/Usin2705/DeepRacer/blob/master/02-Improved-Ln-13.270.py) (13.270s in Cumulo Carrera):

### Core formula: reward = 5.2 + 4*math.log(progress/steps)
(You'll need to import math. Luckily, AWS allow that)

From my understanding, in Reinforcement Learning, you don't need to come up with a sophisticated mathematic formula for your model. What you really need is a reward function, that properly align your target with the reward for each action, and make sure the machine interpret your target correctly (<b>important point</b>)

You can read more about it [here](https://github.com/scottpletcher/deepracer/blob/master/iterations/v4-SelfMotivator.md) (this is from another DeepRacer)

So, since our ultimate target is reaching the finish line as soon as possible, the formular ```4*math.log(progress/steps)``` give higher reward point when progress increase faster than steps. The higher the progress vs 1 specific steps, the higher the reward we get. So if the car take 150 steps to finish the race, its total reward should be higher than the car that took 250 steps. I need to mutiply it by 4 to make the reward smaller (the ```4*math.log(progress/steps)``` return negative number) so the position reward (stay in center line) have significant important.

What about the <b>5.2</b>? Well, since the Natural Logarithm of a number less than 1 (Progress go from 0->100, steps often go from 0->180) is negative, and then multiplying it by 4 making our reward a bigger negative number, adding 5.2 will ensure that our reward will stay positive most of the time.

Our progress reward are often in range of 2.5 to 3.5 point. I also reward the car on position (0~0.8 point). In this model, position reward still play an important role.

## 03 [Improved-Ln-TokyoDrift](https://github.com/Usin2705/DeepRacer/blob/master/03-Improved-Ln-TokyoDrift-11.000.py) (11.000s in Cumulo Carrera):
## 04 [Improved-Ln-TokyoDrift](https://github.com/Usin2705/DeepRacer/blob/master/04-Improved-Ln-TokyoDrift-10.310.py) (10.310s in Cumulo Carrera):
<img src="https://github.com/Usin2705/DeepRacer/blob/master/Leaderboard-virtual-cumulo-carrera-2019-10.310.jpg">


If you check 02, 03 and 04 model, you'll find that the only thing different in those model is that 03 and 04 have smaller position reward (0~0.6) vs (0~0.8). So what's the different?


In 03, I found out that you can actually edit the action space. Instead of using default action space provided by AWS, which use slower speed (2, 4). I open S3 bucket location that contain the model, find the model_metadata.json file, download it, edit it with higher speed (minimum 5) and then upload my new action space to S3 again. We have an awesome DeepRacer Community that willing to help people around, just check out some DeepRacer local training guides, they have a lot of tutorials on how to edit the S3 bucket.

My 03 [model_metadata](https://github.com/Usin2705/DeepRacer/blob/master/03-Improved-Ln-TokyoDrift-11.000-model_metadata.json) with higher speed (lowest speed is 5, highest speed is 8) 

In 04 [model_metadata](https://github.com/Usin2705/DeepRacer/blob/master/04-Improved-Ln-TokyoDrift-10.310-model_metadata.json)
I cut the number of action from 20 down to 8. This would mean faster training time. I also add an action with speed of 9 (which is the highest speed so far) to the model. And I cut 0.69 seconds in my final submission.

With higher speed, the car will start to drift around the track. That's why I called it TokyoDrift.

Now, the formular ```5.2 + 4*math.log(progress/steps)``` is not the best formular to express our target to our machine. Check out the following pictures from local training result using model 04:

13.27 second, higher total reward             |  12 Second, lower total reward
:-------------------------:|:-------------------------:
![](https://github.com/Usin2705/DeepRacer/blob/master/Improved-Ln-TokyoDrift-Canada-13-27s.png)  |  ![](https://github.com/Usin2705/DeepRacer/blob/master/Improved-Ln-TokyoDrift-Canada-12-00s.png)

Notice that the the 12 second run on the right, the one that is better in our view, has lower reward than the 13.23 second. The machine see that wiggle the car around the road will bring better reward, and therefore the more we train our model, the more "wiggling" we'll get. The 12 second is still not the best run we can get, as I can see some corner that the car can cut throught (car don't need to always stay in the center line). The model has room for improvement, however if I train my model more, I'll get more wiggling instead of improvement.

This is because our reward is not 100% aligned with our target, and therefore machine misinterpret it, leading to ineffective model. See the excel analysis from the training log, the reward here is only for ```5.2 + 4*math.log(progress/steps)```:
<img src=https://github.com/Usin2705/DeepRacer/blob/master/Improved-Ln-TokyoDrift-Canada-Analysis-01.png>

The 12 second model have faster start (positive reward from step 6 = higher throttle at the beginning), and generally have higher reward per episode (progress increase faster per step, so car is running faster). However, the slower model stay around the track longer (by wiggling around) and have higher total reward.

One quick solution for this is to change the formula to ```3 + 4*math.log(progress/steps)```:
<img src=https://github.com/Usin2705/DeepRacer/blob/master/Improved-Ln-TokyoDrift-Canada-Analysis-02.png>

As you can see, now the faster model will have higher reward. However, this will bring us at least 13 episodes with 0 reward (from 0 to 12). You will need another reward function from step 0~12, and also what if the car go faster to lower than 11 second, will the fastest still have higher reward? I played with this formular for a while, but in the end I did not get anything good from it.

## 05 [ProgressVelocity](https://github.com/Usin2705/DeepRacer/blob/master/05-ProgressVelocity-08.610.py) (8.610s in Toronto Turnpike):
<img src="https://github.com/Usin2705/DeepRacer/blob/master/Leaderboard-virtual-toronto-turnpike-2019-08.610.jpg">

## Core formula: reward = ((progress- self.pre_progress)*2)**2 + ((progress- self.pre_progress2))**2
Human language: the faster the car increase progress during each of its step, the higher the reward.

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
Solve "ResourceExhaustedError: OOM" problem (hei, if you're at this point at least it work heh):
```
docker exec -t $(docker ps | grep sagemaker | cut -d" " -f1) redis-cli config set client-output-buffer-limit "slave 836870912 836870912 0"
```

SIM_TRACE_LOG explain:

SIM_TRACE_LOG:EPISODE,STEP,X,Y,HEADING(RAD),STEERING(RAD),SPEED,ACTION_INDEX,REWARD,DONE(bool),IS_WHEEL_ON_TRACK(bool),PROGRESS,CLOSEST_WAYPOINTS,TRACK_LENGTH,TIME


  
# Credit:
  
Local training guide from: https://github.com/alexschultz/deepracer-for-dummies (which, in turn, is a wrapper around Chris' repo: https://github.com/crr0004/deepracer). Great work from both of them. Thank you guys for saving me thousands of USD.
  
  
The object class to save previous progress is shamelessly copied from https://github.com/breadcentric/aws-deepracer-workshops.  In this Deepracer community: https://app.slack.com/client/TJKAE89FA/, somebody posted the idea of saving data in AWS' reward function, and another replied with the linked to breadcentric's code. 


Some FAQ for errors: https://codelikeamother.uk/training-locally-for-aws-deepracer-and-a-udacity-challenge-with-rewards
