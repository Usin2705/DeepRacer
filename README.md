# DeepRacer
AWS DeepRacer reward functions and stuffs


# Models explanation
Model stored in this repo are formated this way: xx-ModelName-yy.yyy-Model_Action_Space


xx: ranking of model, the higher the better in actual AWS virtual race

ModelName: The name of model

yy.yyy: Actual shortest completed time in AWS virtual race sumission

Model_Action_Space: Some models come with their specific action space, as they require that action space to have good performance

All model require variables from [InputParameter.py](https://github.com/Usin2705/DeepRacer/blob/master/InputParameter.py). That file contains all possible variable come from DeepRacer. You need to copied all necessary parameter from it to your reward function. InputParameter.py also contains faked params to test out the model and make sure it work.

## 01 [Simple](https://github.com/Usin2705/DeepRacer/blob/master/01-Simple-17.505.py) (17.505s in Shanghai Sudu):
<img src="https://github.com/Usin2705/DeepRacer/blob/master/Leaderboard-virtual-shanghai-sudo-circuit-2019-17.505.jpg">

Just as the title say, very simple model. This model was based on AWS's example model. However, instead of split the car position into 4 (0.1, 0.25, 0.5, and the rest of track will), I split it into 20 markers. I give the first half positive reward (the smaller the different the higher the reward), and the 11-20 negative reward (should not do it). I was in a hurry because I joined the race too late, around 20 August.

Also at that moment I don't have enough time to set up a local training, and don't know how to perform the log analysis. So I have no idea about the car's movement (what a pity). Due to budget reason I already delete the S3 bucket so the record is lost forever :(

## 02 [Improved-Ln](https://github.com/Usin2705/DeepRacer/blob/master/02-Improved-Ln-13.270.py) (13.270s in Cumulo Carrera):

### Core formula: reward = 5.2 + 4*math.log(progress/steps)
(You'll need to import math. Luckily, AWS allow that)

From my understanding, in Reinforcement Learning, you don't need to come up with a sophisticated mathematic formula for your model. What you really need is a reward function, that properly align your target with the reward for each action, and make sure the machine interpret your target correctly (<b>important point</b>)

You can read more about it [here](https://github.com/scottpletcher/deepracer/blob/master/iterations/v4-SelfMotivator.md) (this is from another DeepRacer)

You can also try AWS [sample reward function](https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html#reward-function-input-steps). I believe the idea here is quite the same. You need to twist it a little bit if you want to compete in top 50. For example, my top models alway finish the race with less than 160 steps, so using 300 steps in the example is just too much.

So, since our ultimate target is reaching the finish line as soon as possible, the formular ```4*math.log(progress/steps)``` give higher reward point when progress increase faster than steps. The higher the progress vs 1 specific steps, the higher the reward we get. So if the car take 150 steps to finish the race, its total reward should be higher than the car that took 250 steps. I need to mutiply it by 4 to make the reward smaller (the ```4*math.log(progress/steps)``` return negative number) so the position reward (stay in center line) have significant important.

What about the <b>5.2</b>? Well, since the Natural Logarithm of a number less than 1 (Progress go from 0->100, steps often go from 0->180) is negative, and then multiplying it by 4 making our reward a bigger negative number, adding 5.2 will ensure that our reward will stay positive most of the time.

Our progress reward are often in range of 2.5 to 3.5 point. I also reward the car on position (0-0.8 point). In this model, position reward still play an important role.

## 03 [Improved-Ln-TokyoDrift](https://github.com/Usin2705/DeepRacer/blob/master/03-Improved-Ln-TokyoDrift-11.000.py) (11.000s in Cumulo Carrera):
## 04 [Improved-Ln-TokyoDrift](https://github.com/Usin2705/DeepRacer/blob/master/04-Improved-Ln-TokyoDrift-10.310.py) (10.310s in Cumulo Carrera):
<img src="https://github.com/Usin2705/DeepRacer/blob/master/Leaderboard-virtual-cumulo-carrera-2019-10.310.jpg">


If you check 02, 03 and 04 model, you'll find that the only thing different in those model is that 03 and 04 have smaller position reward (0-0.6) vs (0-0.8). So what's the different?


In 03, I found out that you can actually edit the action space. Instead of using default action space provided by AWS, which use slower speed (2, 4). I open S3 bucket location that contain the model, find the model_metadata.json file, download it, edit it with higher speed (minimum 5) and then upload my new action space to S3 again. We have an awesome DeepRacer Community that willing to help people around, just check out some DeepRacer local training guides, they have a lot of tutorials on how to edit the S3 bucket.

My 03 [model_metadata](https://github.com/Usin2705/DeepRacer/blob/master/03-Improved-Ln-TokyoDrift-11.000-model_metadata.json) with higher speed (lowest speed is 5, highest speed is 8) 

In 04 [model_metadata](https://github.com/Usin2705/DeepRacer/blob/master/04-Improved-Ln-TokyoDrift-10.310-model_metadata.json)
I cut the number of action from 20 down to 8. This would mean faster training time. I also add an action with speed of 9 (which is the highest speed so far) to the model. And I cut 0.69 seconds in my final submission.

With higher speed, the car will start to drift around the track. That's why I called it TokyoDrift.

Now, the formular ```5.2 + 4*math.log(progress/steps)``` is not the best formular to express our target to our machine. Check out the following pictures from local training result using model 04:

13.27 second, higher total reward             |  12 Second, lower total reward
:-------------------------:|:-------------------------:
![](https://github.com/Usin2705/DeepRacer/blob/master/Improved-Ln-TokyoDrift-Canada-13-27s.png)  |  ![](https://github.com/Usin2705/DeepRacer/blob/master/Improved-Ln-TokyoDrift-Canada-12-00s.png)

Notice the 12 second run on the right, the one that is better in our view, has lower reward than the 13.23 second. The machine see that wiggle the car around the road will add more reward, and total higher reward for the whole race, therefore the more we train our model, the more "wiggling" we'll get. The 12 second is still not the best run we can get, as I can see some corner that the car can cut throught (car don't need to always stay in the center line). The model has room for improvement, however if I train my model more, I'll get more wiggling instead of improvement.

This is because our reward is not 100% aligned with our target, and therefore machine misinterpret it, leading to ineffective model. See the excel analysis from the training log, the reward here is only for ```5.2 + 4*math.log(progress/steps)```:
<img src=https://github.com/Usin2705/DeepRacer/blob/master/Improved-Ln-TokyoDrift-Canada-Analysis-01.png>

The 12 second model have faster start (positive reward from step 6 = higher throttle at the beginning), and generally have higher reward per episode (progress increase faster per step, so car is running faster). However, the slower model stay around the track longer (by wiggling around) and have higher total reward.

One quick solution for this is to change the formula to ```3 + 4*math.log(progress/steps)```:
<img src=https://github.com/Usin2705/DeepRacer/blob/master/Improved-Ln-TokyoDrift-Canada-Analysis-02.png>

As you can see, now the faster model will have higher reward. However, this will bring us at least 13 episodes with 0 reward (from 0 to 12). You will need another reward function from step 0~12, and also what if the car go faster to lower than 11 second, will the fastest still have higher reward? I played with this formular for a while, but in the end I did not get anything good from it.

## 05 [ProgressVelocity](https://github.com/Usin2705/DeepRacer/blob/master/05-ProgressVelocity-08.610.py) (8.610s in Toronto Turnpike):
<img src="https://github.com/Usin2705/DeepRacer/blob/master/Leaderboard-virtual-toronto-turnpike-2019-08.610.jpg">

## Core formula: reward = ((progress- self.pre_progress)*2)**2 + ((progress- self.pre_progress2))**2
Human language: the faster the car increase progress during the race, the higher the reward.

Note that there's no other reward in this model, no reward based on current position on the track, no fancy and complex formula to calculate the reward. Car just follow the basic rule, the faster you increase your progress, the higher reward you'll get. In other model, you need to calculate and decide what is the best action for the car so its can run faster, in this model, you set the ultimate goal (go faster) and the car will learn by itself how to do it.

Below is the 11.005 second race in the local training (the best I can get so far in local training is around 10.700s):
<img src=https://github.com/Usin2705/DeepRacer/blob/master/ProgressVelocity-Canada-11-005.png>

Look how close the car near the outside of the track when it turn, notice that it alway target straight line (as I set the highest speed in straight line) whenever possible, and slowdown to make a sharp turn just enough to not go outside of the track and then go straight again. At around 70% of the track, it make a slightly turn on the left and then on the right when it should have go straight for maximum speed. Maybe this is where 305 milisecond different (11.005 vs 10.700s) come from. Which mean I can shorten my time a little bit more.

Overall, the way the car run around the track look like somebody spend a lot of time to calculate the best path possible for the car, but in reality we just use a simple reward function and the car found out the best path by itself.

The model also have some problem as well. Remember that we didn't train on the submission track, we trained on a different track and in the submission we test if our car can run on another track. AWS do this to avoid overfit problem. Since the car always prefer to cut corner and run fast, and I spent a lot of time to train the model to get the fastest result, most of the time in the submission track the car cut corner a little bit too far and went outside of the track. So it's fast but not a reliable model. However, this is typical problem if you want you car to go less than 9 seconds, you have to raise your car speed, and car has to  cut cornet a lot.

I'm thinking of setting a punishment for the car if it cut the corner too close to the outside (For example, setting maximum distance from the middle line of 40% of the track width, if the car go outside 40% then change reward to 0). This way the car can still cut corner, but it stay inside the track so it's much safer.

Also, the reward function can be improve a little bit, that formula is not as good as I think it is.  Now after the rush to 31 October deadline, look at the formula again calmly, I think I should not use "power by 2" in the formular, I think it's too aggressive.

Action space is also something I should change. This model take a really long time to train so I only use small action space to save time. So the car was limited to a few actions that <b>I think</b> are the best, and that's not good. Car should be able to decide which actions is the best for this race, therefore I must give them much more options to choose.

### After the November race, AWS increase the racing track width. Bigger width mean you can increase your speed more without the car go off track. So I'm trying to experiment with the new limit on car speed

# Hyperparameters:

I don't really know much about hyperparameters, so I can only talk about a few that I think I know:

## Learning rate:

The learning rate for each run, the default 0.00035 is pretty good so at first you can use it. After a while when your model not improving anymore, you can fine tune it by lower the learning rate to 0.00015 or lower. Beware of the overfit problem, though. The more you train your model in the same track, the higher chance your model will over fit into that track. And when you make submission to AWS hidden track, its performance will become terrible.

## Discount factor:

The weight of the future reward of your future action to the total reward. Let's say your current action reward is 20 (step 1), and your next action (step 2) reward is 10, and the next action (step 3) reward is 15. With discount rate of 0.99, your total reward is: 20 + 0.99^1*10 + 0.99^2*15

So with the default discount rate of 0.999, and a normal race took about 200 steps, your last step reward will be mutiply with 0.999^200 = 0.819 time compared with your first step. And this is not needed. You don't really need to look that far. I use discount factor of 0.99, so my last step reward will be 0.99^200 = 0.134 time compared with my first step. 0.134 is pretty small so my car tend to ignore the last steps and focus more on nearest steps. 

Another example, I want to make sure my car take the sharp turn properly without fail, and so it need to look into future steps. You need to slowdown much earlier with the car running at high speed, so you can make a quick turn and then speeding again. During a run, steps 60 to 90 is when it make the sharp turn, from when it slowing down to when it start speeding again. When my car stay at 60 steps, the 90-Step (with the discount factor of 0.99) is 0.99^30 = 0.74 time smaller compared with my 60-Step, smaller but still significant. If I use discount factor of 0.91, my 90-Step only equal to 0.91^30 = 0.06 time compared with my 60-Step, so my 90-Step will be ignore. This is not my desired target, as I want my car to make sure the turn from 60 to 90 steps go smoothly.

If you want you can still use discount factor of 0.999, but from my experience (or maybe just a pseudo effect), lower discount factor a little will improve your model. However, don't lower it too low (less than 0.90) as it not recommended


# AWS DeepRacer
Thank Amazon for this wonderful experience. I learn a lot about AWS, Linux and Reinforcement Learning from the race, met wonderful people online, participating in a very challenging race until the end (that feeling when people start to kick you down  and out of the top 20. Or every morning when you woke up, opened the console and saw another person reach 7.xxx second while you struggling with 8.6 \*O\*  )

The 2020 will would be much more exciting. Now you can change the Reinforcement Learning method instead of using PPO. This will be a good motivation to learning more. There will be 2 more type of race (passing objects and 2 car race toghether). Car now have a LIDAR sensor as well.

## My own corner, to store my own things:
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

### Iteration n is saved to model n
### Positive steering = turn left, negative steering = turn right (wth?)

SIM_TRACE_LOG explain:

SIM_TRACE_LOG:EPISODE,STEP,X,Y,HEADING(RAD),STEERING(RAD),SPEED,ACTION_INDEX,REWARD,DONE(bool),IS_WHEEL_ON_TRACK(bool),PROGRESS,CLOSEST_WAYPOINTS,TRACK_LENGTH,TIME


  
# Credit:
  
Local training guide from: https://github.com/alexschultz/deepracer-for-dummies (which, in turn, is a wrapper around Chris' repo: https://github.com/crr0004/deepracer). Great work from both of them. Thank you guys for saving me thousands of USD.
  
  
The object class to save previous progress is shamelessly copied from https://github.com/breadcentric/aws-deepracer-workshops.  In this Deepracer community: https://app.slack.com/client/TJKAE89FA/, somebody posted the idea of saving data in AWS' reward function, and another replied with the linked to breadcentric's code. 


Some FAQ for errors: https://codelikeamother.uk/training-locally-for-aws-deepracer-and-a-udacity-challenge-with-rewards
