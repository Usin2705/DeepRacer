# DeepRacer
AWS DeepRacer reward functions and stuffs

# 2019 model and more detail explanation
Click on the [2019](https://github.com/Usin2705/DeepRacer/edit/master/2019/) folder for a more detail explanation on why did I choose that type of reward function.
In 2020, I did not have enough time to come up with a better model, so I just use the old model from 2019 (with a minor modification)


# 2020

Find the [2020 model here](https://github.com/Usin2705/DeepRacer/blob/master/ProgressVelocity.py)
There're a lot of change in the 2020 race, but I did not change my reward function. The only small thing you need to change here is "A" and "B". The track is longer so you need to increase A and decrease B to get a good reward. Good reward here mean if the car go fast then the reward should be big, and vice versa. I changed the value so much so I did not remember the exact value I used for my model :(

The reason of using this old reward function is simply because I failed to get a better one, due to time limit (the optimization is longer vs last year, I was busy with work and study) and it's hard to find a good reference value (more on this later). 

But please note that the reward fucntion here is still <b>need improvement.</b>

Nevertheless, with just 5 days training, I got a very good result in September virtual race. I even make it to the semifinalist of the head-to-head racing. Although it's fair to mentioned that all the champion from previous races are excluded from the September race =)). 

<img src="https://github.com/Usin2705/DeepRacer/blob/master/Leaderboard-virtual-cumulo-turnpike-2020-79.546.png">

My September model was not optimized (you can see that it went outside of track all the time) and my October model was worse because I was experimenting a new strategy. If you spend your time just to train this model, you could get better result than I did. 

<img src="https://github.com/Usin2705/DeepRacer/blob/master/Leaderboard-virtual-stratus-loop-2020-106.204.png">

Anyway, if you look at the picture of a training (it's 2nd highest reward, ideally it should be the highest but the model was not optimized), you can see that from a very simple reward function, the model has learn on how to cut corner and drive straightforward (red circles) (the drive straight have the fastest speed).

<img src="https://github.com/Usin2705/DeepRacer/blob/master/ProgressVelocity-stratus-loop-40-000.png">

## Some ideas on how to improve the reward function:

You need to to map your progress with a reference. Here in my model, I mapped it with with step. So if the progress is bigger in this step vs last step, we increase the reward. However, step is not a reliable reference. It varies depend on the speed of your car. If the car run very fast (which is a very good thing), you will have less step and less total reward (not good, we want high total reward if car is fast). If the car run slowly (which is not good), you will have many steps and could have a high total reward (not good in this case).

Ideally, you want your reference to be time. Your progress is displacement x, your reference is time t. Your reward is velocity v = x/t. Higher velocity = faster and also mean higher reward. The problem is you can not use time in AWS deepracer console (you can't import time), so you can only train it with local training or cloud training (most people are not using only AWS console anyway). Also time might not consistent between training (you might try rospy.get_time() as well) because there's a small time lag between each iteration. I spent 80% of the time in September and $300 AWS credit to experiment with the progress/time but did not get a good result from it. It could due to other reason as well, since I also messing around with lidar and stereo camera, so I'll try it again next year.

You can also use step as reference, as long as you aware of its problem, and I'm thinking of a way to address that proble. Hopefullly it'll work next year =)) 

## Some changes in 2020 track and tips:

The track is much longer, about 3 times or 4 times of the 2019 track. As a result, the time you need to optimize your model is also longer. It's more difficult to have a good model in the competition (but also more interesting, the 2019 track was too short so there's a lot of luck factor in it). I think now it would take me about 10~15 days to get a good optimized model (last year it was just 1 week). 

You're no longer disqualified if you out of track, instead, you get a penalty (5 seconds). This change is very good IMHO. We no longer need to gambling or spam submit to get the 100% perfect race, and instead we can choose between faster (with risk of getting a penalty) vs slower and without penalty.

There're 3 different mode. And 3 modes make optimizing a model way way more difficult (in addition to the longer track = longer optimization time). What I did was just train on the time trial track, and if you get a good result you can submit it to object-avoidance or head-to-head. Because the optimization time is too long, I didn't have time to train the optimized time-trial model with object-avoidance or head-to-head, so I'm not sure if it improve the model or not.

There are new stereo camera, lidar (and even a deeper neural work model). I enjoy the new idea, but after wasting a month without any good result, I have to switch back to the pure "front-facing camera". Well, it was not the fault of the stereo camera or lidar, but I found that the front-facing camera converge faster, and it's good enough. Remember that the 2020 track is long and will take a long time to find an optimized model, so if you could save time then you should :)

Due to the longer track, you should focus on minimize your action space - the "model-metadata.json" file. bigger action space lead to significant longer time to train an optimized model (and that's why you don't use AWS action space, but use your own customized action space). I'm targeting my action space to below 7 actions (or maybe lower???) to save time on training.

# Credit

[AWS Deepracer Community](https://deepracing.io/): This is where you can find all the useful info and dicussion

[Larsll deepracer for cloud](https://github.com/larsll/deepracer-for-cloud): I used his repo in September when I was blessed with AWS credit

[Mattcamp deepracer local](https://github.com/mattcamp/deepracer-local): I used his repo when I run out of AWS blessing :D






