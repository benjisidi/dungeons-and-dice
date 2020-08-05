# Dungeons and Dice

Fun with the mathematics of dice rolling, in the context of Dungeons and Dragons

[toc]

## Basic rolling

To begin, I would like to roll:

1. A die
2. A collection of dice
3. (1) and (2), n times.

(1) is easy - to “roll” a die with *f* faces, simply choose a random integer between 1 and *f*:

```python
result = random.randint(1, f)
```

This extends to (3) straightforwardly - just repeat *n* times

```python
# Note: While (f, n=1) might make more sense, the order of args here lines up nicely with
# the "ndf" (eg 1d6 = "one six-sided die") notation used regularly in dnd
def roll(n, f):
    return [random.randint(1, f) for i in range(n)]
```

To tackle (2), I define a ***cluster*** of dice (a collective noun I stole from diamonds and quite like) as a list of `(n, f)` tuples, each denoting *n* dice with *f* faces. For example, `1d4 + 2d6` in dnd terms (one four-sided die, and two six-sided dice) form the cluster

```
1d4 + 2d6 = [(1, 4), (2, 6)]
```

Using this, we can roll a cluster by simply calling `roll` on each of its elements. To roll a cluster more than once, we repeat this *n* times.

```python
def roll_cluster(dice_list, n=1):
    return [[roll(n, f) for (n, f) in dice_list] for i in range(n)]
```

## Expected results

In theory, using just the `roll_cluster` method, we could compute the answer to any question about dice rolling we had by simulating it. Simulation is (most of the time) both less efficient and less precise than analytic solutions (imagine we want to find the expected result of rolling a 1e6d100 - we have to generate a million random numbers and sum them for each trial, and then perform enough trials to get a reasonable result…). We can be much more performant by working with probabilities to solve problems exactly.

### The expected result of rolling a single die

The expectation of a random variable is equal to the sum of all possible outcomes multiplied by their respective probabilities. In the case of rolling a die, the outcomes are the values of the faces, and the probability of each is constant at $\frac{1}{f}$
$$
E(1df) = \sum_{i=1}^{f} \frac{1}{f}i = \frac{1}{f} \sum_{i=1}^{f} i
$$

### The expected result of rolling *n* dice

The expectation of *n* rolls is just the expectation of a single roll multiplied by *n*
$$
E(ndf) = n\sum_{i=1}^{f} \frac{1}{f}i = \frac{n}{f} \sum_{i=1}^{f} i
$$
We can use the fact that the sum of a range of numbers `[1, n]` is the average of the first and last number, multiplied by the length of the range to simplify our expression and remove the sum
$$
\begin{alignat}{1}
\sum_{i=1}^{f} i &= \frac{f+1}{2}f \\
\implies E(ndf) &= \frac{n}{f} \frac{f+1}{2}f \\
 &= n\frac{f+1}{2}
\end{alignat}
$$
or in Python (repeating for each set of dice in our cluster)

```python
def expected_result(dice_list):
    return [n * (f + 1) / 2 for (n, f) in dice_list]
```


