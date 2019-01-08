# CHSH

This is a readme for our CHSH inequality experiments.

## Circuit naming convention

For CHSH experiments following circuit naming convention shall be used:

```
CHSH_measurement_theta
```

where CHSH is the basic name of experiments, measurement denotes what's being measured, theta is the angle (in radians) of rotation
around Y axis. For example

```
CHSH_XX_0.62
```

means that the experiment was CHSH XX experiment with rotation 0.62 around Y axis. 

Note that CHSH inequalities check in methods.py is reduced to 

```
CHSH-test_measurement
```

only as it's not as detailed as these experiments.

