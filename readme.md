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
def roll_cluster(cluster, n=1):
    return [[roll(n, f) for (n, f) in cluster] for i in range(n)]
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
def expected_result(cluster):
    return [n * (f + 1) / 2 for (n, f) in cluster]
```

## Successes and failures

We can now performantly calculate the expected result of any arbitrary cluster of dice, which is quite nice (for example, if we want to know the average damage of a particular weapon). When playing, we’re often more interested in rolling *at least some threshold value*. Ability checks, attack rolls and saving throws all depend on this mechanism. To do this, we’re going to need to be able to calculate the number of ways of rolling a given value using a cluster.

### Probability of rolling exactly *t* on *n* identical dice

To tackle this, we’ll use generating functions as it is by far the most straightforward way to do it, and results in quite neat code ([click here](https://www.youtube.com/watch?v=n9FFBXBccow) for a quick introduction to what generating functions are).

The generating function for *1df* is 
$$
G(x, 1, f) = x^1 + ... + x^f
$$
since we have a single way of rolling any value in $[1,f]$. To get the generating function for *ndf*, we simply take this to the n^th^ power:
$$
G(x,n,f) = (x^1 +...+x^f)^n
$$
The number of ways of getting $t$ when rolling $ndf$ is simply the coefficient of $x^t$ in $G(x,n,f)$. For convenience going forward, we’ll call this quantity 
$$
\begin{align}
N(t,n,f) &= \textit{# of ways of rolling t on ndf} \\
 &= \textit{coefficient of $x^t$ in $G(x, n, f)$}
\end{align}
$$
Conveniently, numpy has a very fast function for evaluating powers of polynomials:

```python
np.polynomial.polynomial.polypow(poly, power)
```

returns an array of the coefficients of the resulting polynomial in ascending order. After catching the trivial cases, we can use it to evaluate the # of ways of rolling any quantity we wish:

```python
def N(t, n, f):
    if t > n * f or t < n:
        return 0
    if t == n * f or t == n:
        return 1
    return np.polynomial.polynomial.polypow([0, *[1 for i in range(f)]], n)[t]
```

The *probability* of rolling a exactly $t$ on $ndf$ is $N(t, n, f)$ divided by the total number of possible rolls, which is just $f^n$:
$$
p(t,n,f) = \frac{1}{f^n}N(t,n,f)
$$

### Probability of rolling exactly *t* using an arbitrary cluster of dice

We now need to extend our expressions for $N$ and $p$ to arbitrary clusters. Imagine we are trying to roll a target total $t$, and have already rolled dice totalling $s$. This means we have $r = t - s$ remaining. On our next roll:

1. The maximum we can roll on the current set assumes we roll the minimum value (one * number of dice) for all subsequent sets.
2. The minimum we must roll on the current set assumes we roll the maximum value (number of faces * number of dice) for all subsequent sets.

This means we can calculate the number of ways of getting $t$ by calculating the number of ways to get the minimum roll on the first set, added to all valid subsequent rolls on the second set, etc.



### Probability of rolling greater than a threshold value on a single die

This is the simplest and most straightforward problem - what is the probability of rolling greater than *t* on *1df*. In dungeons and dragons, we are more often concerned with rolling *at least/greater than or equal to* some value - but the problem stated in the above form is more neatly solved, and one can simply subtract one from the desired threshold to obtain the same result - so we’ll stick with *greater than* for now.

The probability of rolling greater than $t$ on *1df* is the number of faces greater than *t*, divided by the total number of faces.
$$
p(1df \gt t) = \frac{f-t}{f} = 1-\frac{t}{f}
$$



### Probability of rolling greater than a threshold value on *n* identical dice

Here things get interesting: we want *the number of results that sum to greater than t, divided by the total number of possible results*. The second quantity is easy to calculate
$$
\textit{# of possible outcomes from ndf dice} = f^n
$$
To get the first quantity, we’ll need to begin with the number of results that sum to a specific quantity, and then add those up. To simplify our notation, let’s define *“the number of ways of rolling x on ndf”* as $N(x, n, f)$. Using this:
$$
\begin{align}
N(x, n, f) &= 0 \;\; x \le 0 \label{invalidRolls} \\
N(x, 1, f) &=
	\begin{cases}
		1 & 0 \lt x \le f \\
		0 & otherwise
	\end{cases} \label{singleRoll} \\
\end{align}
$$
($\ref{invalidRolls}$) states that the number of ways of rolling 0 or below on any number of dice is zero. ( $\ref{singleRoll}$) states there is one way to roll each valid number on a single die. At this point, we’re going to keep running into piecewise functions wherever we have to worry about numbers being “valid”. To avoid this muddying the algebra, from now on we’ll assume the results and dice we are attempting to roll are reasonable. In practice, we’ll want to catch these to make sure our code doesn’t fall over on invalid input, and instead reports, for example, that the probability of rolling a 7 on $1d6$ is 0.
$$
\textit{When calculating $N(x,n,f)$, we assume} \\
n \le x \le nf \\
\textit{and when summing rolls $\sum_{x=a}^{b}f(x)$, we assume} \\
a \le b
$$
Given these, we can look at the number of ways to roll greater than a threshold $t$ on $1df$:
$$
N(\gt t, 1, f) = \sum_{i=t+1}^{f} N(i,1,f) = f-t \label{singleSum}
$$
($\ref{singleSum}$) states the sum of the number of ways to roll greater than $a$ on $1df$ is simply the difference between $f$ and $t$. This makes sense intuitively - if we want to roll greater than $t$, we take the the total number of possible rolls ($f$) and subtract the number of rolls less than or equal to $a$, which is a sequence $[1, t]$ of length $t$.

Next, let’s extend this to two dice. If I want to roll greater than $t$ on two dice and the most I can roll on a single die is $f$, I must roll at least $t-f$ on the first roll. If on the first die I roll $i$, I must then roll $t - i$ on the second die to get $t$.
$$
\begin{align}
N(>t,2,f) &= \sum_{i=t-f}^{f}N(i,1,f)N(t-i,1,f) \\
 &= \sum_{i=t-f}^{f} 1 \\
 &= f - (t - f) \label{doubleSum} \\
 &= 2f - t 
\end{align}
$$
($\ref{doubleSum}$) basically states *the number of ways to roll greater than t on two dice is equal to the number of valid first-die rolls*, which again makes sense intuitively.

To extend this to higher numbers of dice, we’re going to need an expression for the number of ways to roll a *particular* value, rather than *greater than* a value. We can apply the same logic here: if I wish to roll exactly $t$ on two dice, the minimum value for my first roll $i$ is $t-f$ and my second roll is fixed at $t-i$. Additionally, the *maximum* value for my first roll is $t-1$, since I can’t roll a 0 on the second die. So, the total number of options is $len([t-f, t-1]) = t-f - (t-1) + 1$. We arrive at almost the same expression, just with slightly different limits: len([t-f, t-1]) t-1 - t-f = f - 1
$$
\begin{align}
N(t, 2, f) &= \sum_{i=t-f}^{t-1} N(i, 1, f)N(t-i, 1, f) \\
 &= \sum_{i=t-f}^{t-1} 1 \\
 &= (t - 1) - (t - f) \\
 &= f - 1
\end{align}
$$


Let’s extend this one more time to $3df$, and then see if we can get a general solution for $ndf$.
$$
\begin{align}
N(\gt t,3,f) &= \sum_{i=t-2f}^{f} N(i,1,f)N(t-i,2,f) \\
 &= \sum_{i=x-f}^{f}
\end{align}
$$
