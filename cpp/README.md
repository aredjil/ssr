# Sample Space Reducing Process 

## Table of Content 
- [Introduction](#introduction)
- [Sample Space Reducing Processes](#sample-space-reducing-processes)
  - [Sample Space Reducing Processes](#sample-space-reducing-processes)
  - [Sample Space Reducing Process Cascades](#sample-space-reducing-processes-cascades)
  - [Noisy Sample Space Reducing Processes](#noisy-sample-space-reducing-processes)

- [Conclusion](#conclusion)
- [Refrences](#refrences)
- [Appendix](#appendix)

## Introduction: 

Many complex systems follow a ubiquitous pattern, namely power law,

$$
P(R=r) \propto \frac{1}{r^{\alpha}}
$$

In language, this appears as Zipf's law: The frequency of occurance of a word in a corpus decreases as a power of their rank ($\alpha \approx 1$). In other words, a small set of words account for most of language usage, while the higher the rank the rarer it becomes, but not as rare as exponential decay would suggest, making the distrubution heavy-tailed. However, power laws are not unique to language, they are observed in many other phenomena, such as city sizes, earth quake magnitude, wealth distrubution, and severity of terrorist attacks.

<!-- NOTE: Decrease the size of the figure to something small that does not take the bulk of the document -->

<div style="text-align: center;">
    <img src="./results/figures/words_count_in_books.png" alt="Zipf's law" width="400">
    <p><em>Zipf's law observed in word counts across 20 books. The books taken from <a href="https://www.gutenberg.org/">Project Gutenberg</a>, , and the results are fitted using powerlaw package [5]</a>.</em></p>
</div>

The origin of power laws is still debated, many attempts have been done to explain their emergence like Preferential attachment, Mandelbrot's Model, and  sample space reducing processes.

## Sample Space Reducing Processes

There are many flavors of SSR process, each producing a range of power laws, they are all charchterized by a shrinking sample sapce $\Omega$. In the following subsections I will present three SSR proceses, namely: standard SSR, noisy SSR, and SSR cascade. And show the results of the numerical simulations. 

### Standard SSR

The standard SSR $\phi$ is defined on a sample space with $N$ states $\Omega = \{N, \dots, 1\}$, each with a prior probability $\pi_i$ of appearing. The process starts at $X_0=N$, at each discrete time step $t>0$ the process jumps randomly following a transition probability $P(X_{t+1}=i\mid X_{t} =j) = p(i \mid j)$ to lower states $j < i$, where upward jumps are forbidden. When the process reaches the states $X_{t>0} = 1$ the process either stops or restarts. 

The process is charchterized by a shrinking samples, where the cardinality of the space is  

$$
\mid \Omega_1 \mid <  \mid \Omega_2 \mid < \dots < \mid \Omega \mid 
$$ 


And the strcutre is nested 

$$
\Omega_1 \subset \dots \subset \Omega_i \subset \Omega
$$

Conceptually, one can imagine a staircase with $N$, the ball starts at the highest step $N$ and can only move downward until it reaches the last step, where the process either stops or restarts. 

<div style="text-align: center;">
    <img src="./results/figures/gif/std_ssr.gif" alt="Zipf's law" width="400">
    <p><em>SSR animation, showing the stair case pictorial formulation using a unifrom one-jump kernel and prior.</em></p>
</div>


It has been shown that the probability of visiting the state $i$ is an exact Zipf's law [[1](https://arxiv.org/pdf/1407.2775)]. 

$$
p(i) =  i^{-1}
$$


<div style="text-align: center;">
    <img src="./results/ssr_graph_3.png" alt="3Ns" width="400">
    <p><em>SSR for 3 states showing the different paths of the process.</em></p>
</div>

In the case of langauge, sentence formation is constrained by the language grammar. At the start of the document, one can use any word corresponding to the intial sample space, once a word is chosen the next word choice is constrained by the grammar of the  language, writer's style, ... etc. Which suggest that the emergence of Zipf's law in language is due the nested structure of possible words.

**Results:**

The numerical simulation confirms this result: running the standard SSR process with $N = 10^4$ states for \(M = 10^6\) restarts produces a histogram of visits that visually resembles a power law, and fitting the data using MLE [[2](https://arxiv.org/abs/0706.1062)] suggests that Zipf's law is a good fit, which is further supported when visualizing the word counts in *Moby-Dick* alongside the SSR process with $10^4$ states and $2 \times 10^4$ restarts.

<div style="display: flex; justify-content: center; align-items: flex-start; gap: 20px;">

  <div style="text-align: center;">
    <img src="./results/figures/std_fit.png" alt="SSR fit" width="400">
    <p><em>Zipf's law observed in SSR state visits frequency.</em></p>
  </div>

  <div style="text-align: center;">
    <img src="./results/figures/moby_word_ssr.png" alt="Moby-Dick Word SSR" width="400">
    <p><em>Word count and SSR state counts vs rank</em></p>
  </div>
</div>


I found numerically that the shape of the state visits distrubution is senstive to the choice of the transition probability $p(i \mid j)$, where in the first expriment I used a gap based transition $p(i \mid j) \propto (j-i)^\alpha$ where the jumps depends on the distance between the current state $X_{t} =j$ and the next state $X_{t+1} = i$ where the exponent $\alpha$ controls perfered states,

- $\alpha = 0$ The process reduces to the standard SSR with perfect Zipf's law
- $\alpha > 0$ Higher states are prefered. 
- $\alpha <0$   Lower states are prefered. 

Fitting the data using MLE shows that the distrubution follows a truncated power law with exponent $-1$. 

  <div style="text-align: center;">
    <img src="./results/truncated_powerlaw.png" alt="non-uniform pij" width="400">
    <p><em>SSR state counts vs rank using a non-uniform transition.</em></p>
  </div>
</div>

In another expriement I used the softmax as a transition probability $p(i\mid j) \propto e^{-\beta i}$. 

- $\beta = 0$ Transitions are uniform, $p(i) = i^{-1}$
- $\beta < 0$ Transitions favor lower states.  
- $\beta > 0$ Transitions favor higher states.  


  <div style="text-align: center;">
    <img src="./results/exp_ssr.png" alt="Exp pij" width="400">
    <p><em>SSR state counts vs rank using a non-uniform transition.</em></p>
  </div>
</div>

When using uniform prior and transitions, stadard SSR generates perfect *Zipf's law*. However, numerical results show that the process is senstive to transition probability.  In the case of using a gap based transition the distrubution follows a truncated power law instead. 

### Noisy SSR 

Now let us consider another variation of SSR where noise is incorporated. Noisy SSR $\mathbf{\Phi}^{(\lambda)}$ is a mixture of the standard SSR $\phi$ with an unconstrained random walk $\phi_R$, according to a mixture parameter $\lambda \in [0, 1]$ which controls the noise strength, 

$$
\mathbf{\Phi}^{(\lambda)} = \lambda \phi + (1-\lambda) \phi_R
$$

It is clear that, 

- $\lambda = 0$ The process is identical to a standrd SSR
- $\lambda = 1$ The porcess is the unconstrained random walk over the states

In this formulation, the process has two options at each time step $t > 0$, to jump downward with probability $\lambda$ or to jump to any of the $N$ states with probability $1-\lambda$. The process keeps going untill the state $1$ is reached. In order to be able to study the stationary statstics of this process, we need to redfine the process $phi$ as $phi_{\infty}$ that is identical except at the state $1$ instead of stoping the process restarts at any one of the $N$ states. 

$$
\mathbf{\Phi}^{(\lambda)}_{\infty} = \lambda \phi_{\infty} + (1-\lambda) \phi_R
$$

This tweal makes it possible to treat the process as stationary. We are intrested in the visiting probability $p^{(\lambda)}(i)$ which could be expressed as 

$$
p^{(\lambda)}(i) = \sum\limits_{j=1}^{N}p(i \mid j)p^{(\lambda)}(j) 
$$

Where the traisntion probability $p(i \mid j)$ is expressed as 

$$
p(i \mid j) =
\begin{cases}
\dfrac{\lambda}{j-1} + \dfrac{1-\lambda}{N}, & i < j,\\[6pt]
\dfrac{1-\lambda}{N}, & i \ge j > 1,\\[6pt]
\dfrac{1}{N}, & j = i.
\end{cases}
$$

Then,  

$$
p^{(\lambda)}(i) = \dfrac{1}{N}p^{(\lambda)}(1)+\sum\limits_{j=2}^{i}p(i \mid j) p^{(\lambda)}(j) + \sum\limits_{j=i+1}^{N}p(i \mid j) p^{(\lambda)}(j)
$$

Pluggin in the different expression of the different state ranges we get,

$$
\begin{align}
p^{(\lambda)}(i) &= \dfrac{1}{N}p^{(\lambda)}(1)+\sum\limits_{j=2}^{i} ( \dfrac{\lambda}{j-1} + \dfrac{1-\lambda}{N} ) p^{(\lambda)}(j) + \sum\limits_{j=i+1}^{N}\dfrac{\lambda}{j-1} p^{(\lambda)}(j) \nonumber\\
&= \dfrac{1-\lambda}{N}+ \dfrac{\lambda}{N}p^{(\lambda)}(1) +\sum\limits_{j=i+1}^{N}\dfrac{\lambda}{j-1} p^{(\lambda)}(j) \nonumber
\end{align}
$$

Now substituing the value $i+1$ we get, 

$$
p^{(\lambda)}(i) = \dfrac{1-\lambda}{N}+ \dfrac{\lambda}{N}p^{(\lambda)}(1) +\sum\limits_{j=i+1}^{N}\dfrac{\lambda}{j-1} p^{(\lambda)}(j) 
$$

Which results in, 

$$
p^{(\lambda)}(i+1) - p^{(\lambda)}(i) = -\dfrac{\lambda}{i} p^{(\lambda)}(i+1) 
$$

Rearranging the results gives, 

$$
p^{(\lambda)}(i+1) = (1+\dfrac{\lambda}{i})^{-1}p^{(\lambda)}(i)
$$


$$
\begin{align}
\dfrac{p^{(\lambda)}(i)}{p^{(\lambda)}(1)} &= \prod_{j=1}^{i-1} (1+\dfrac{\lambda}{i})^{-1} \nonumber \\
&= \exp{(-\sum\limits_{j=1}^{i-1}\log(1+\dfrac{\lambda}{i}))}\nonumber\\
&\sim \exp{(-\sum\limits_{j=1}^{i-1}\dfrac{\lambda}{i})}\nonumber\\
&\sim \exp{(-\lambda \log(i))}\nonumber
\end{align}
$$

$$
\boxed{p^{(\lambda)}(i) \propto i^{-\lambda}}
$$


**Results**

Simualting the noisy SSR using $10^4$ states with $10^6$ runs we get that the numerical results are in accordance with the analytical solution. 


<div style="text-align: center;">
    <img src="./results/figures/noisy_fit.png" alt="Noisy SSR" width="400">
    <p><em>Noisy SSR</em></p>
</div>


### SSR Cascades

The SSR cascades is defined by $\mu$ balls starting at the top state $N$, jumping to any of the lower states, where each state has a unique prior probability of appearing, in the next jump each ball divides into $\mu$ new balls and jump any lower state with respect to their parent ball. The process continues untill all balls reach the terminal state $1$. 

The frequency of state visits has been found to follow a power law with $\mu \in [0, \infty]$ being the exponent [paper](https://arxiv.org/pdf/1703.10100). 

$$
\boxed{p(i) \propto i^{-\mu}}
$$


<div style="text-align: center;">
    <img src="./results/figures/gif/casecade_ssr.gif" alt="Cascade SSR" width="400">
    <p><em>An animation of the SSR Cascades with multiplicative factor of 2</em></p>
</div>


**Results:**

For the numerical simulation the process starts with $1$ element at the top state $N$, at each time step the object divides into $\mu$ new balls, and the process reapeats untill all elements reach the state $1$. In the case where $\mu$ is a real number, we decompose it as $\mu = \lfloor \mu \rfloor + \delta$, with probability $\delta$ the element divdes into $\lfloor\mu\rfloor + 1$ objects and with probability $1-\delta$ the object divides into $\lfloor\mu\rfloor$ objects. 

Numerical results support the analytical results: 

$$
p(i) \propto i^{\mu}
$$

<div style="text-align: center;">
    <img src="./results/figures/figure1/state_visits_relative_frequency.png" alt="Cascade SSR" width="400">
    <p><em>Cascade SSR using different values of the multiplicative factor.</em></p>
</div>


Defining the avalanche size $s$ as the number of elements produced by the SSR cascade $\phi^{(\mu)}$ that reachs the terminal state $1$, the cascade size dsitrubution $f(s)$ seems to follow a gamma distrubution $\Gamma$ [paper](https://www.nature.com/articles/s41598-017-09836-4).  

$$
f(s) \propto s^{\alpha -1}e^{-\lambda s}, <s> \propto \dfrac{N ^\mu}{e^{a\mu}}
$$

The numerical results seem to agree. 

<div style="text-align: center;">
    <img src="./results/figures/figure3/avalanche_sizes_2.0.png" alt="Cascade SSR" width="400">
    <p><em>Distrbution of of avalanche size using a multiplicative factor 2. And its gamma fit</em></p>
</div>


<div style="text-align: center;">
    <img src="./results/figures/figure3/average_size.png" alt="Cascade SSR" width="400">
    <p><em>Avalanche size of Cascade SSR for different total number of states N vs the multiplicative factor.</em></p>
</div>

## Conclusion



## Refrences 

## References  

[1] [Sample space reducing cascading processes produce the full spectrum of scaling exponents](https://arxiv.org/abs/1602.05530)  
Bernat Corominas-Murtra, Rudolf Hanel, Stefan Thurner  

[2] [Understanding scaling through history-dependent processes with collapsing sample space](https://arxiv.org/abs/1407.2775)  
Bernat Corominas-Murtra, Rudolf Hanel, Stefan Thurner  

[3] [Sample space reducing processes produce the full spectrum of scaling exponents](https://arxiv.org/abs/1703.10100)  
Bernat Corominas-Murtra, Rudolf Hanel, Stefan Thurner  

[4] [Power-law distributions in empirical data](https://arxiv.org/abs/0706.1062)
Aaron Clauset, Cosma Rohilla Shalizi, M. E. J. Newman

[5] [Powerlaw: a Python package for analysis of heavy-tailed distributions](https://arxiv.org/abs/1305.0215)
Jeff Alstott, Ed Bullmore, Dietmar Plenz


## Appendix 

An alternative derivation of the state visits distrubution expression for a randomly chosen intial state values $X_0$ \in \Omega.  

- $p(i|j)$ The one-jump transition probability from state $j$ to state $i$, it is uniform in the standard SSR: 
  $$
  p(i|j) =
  \begin{cases}
  0, & j < i, \text{Upward transitions are unallowed,} \\[6pt]
  \dfrac{1}{j-1}, & j > i, \text{Jump uniformly to lower states}.
  \end{cases}
  $$
- $P(X_{0}) = \pi_j$ The probability of starting the process at state $j$ 
- $P(X_{t>0}=i \mid X_{0}=j) = T(i \mid j)$ The probability of visiting a state $i$ if the process starts at $j$:

  $$
  T(i \mid j) =
  \begin{cases}
  1, & j = i,\\[6pt]
  0, & j < i,\\[6pt]
  \sum\limits_{k=1}^{j-1}p(k\mid j)T(i \mid k), & j > i.
  \end{cases}
  $$

In the case of uniform one-step jumps to lower states we can write the the transition probability $T(i\mid j)$ in a clean way. 

For $j>i$ we have 

$$
\begin{align}
T(i\mid j) &= \sum\limits_{k=1}^{j-1}p(k\mid j)T(i \mid k)\nonumber\\
    &=\sum\limits_{k=1}^{j-1}\dfrac{1}{j-1}T(i \mid k)\nonumber\\
\end{align}
$$

The base case for which is $T(i\mid i) =1$. When we consider the case $j=i+1$

$$
\begin{align}
T(i\mid i+1) &=\dfrac{1}{i} \sum\limits_{k=1}^{i}T(i \mid k)\nonumber\\
T(i\mid i+1) &=\dfrac{1}{i} \nonumber
\end{align}
$$
We get the last result because all terms are zero except for the term $T(i|i)$. 

Following the same logic we can prove by induction that the same formula hold for $J > j$.

The general expression of the visiting probability of state $i$ is then

$$
\boxed{p(i) = \pi_i + \sum\limits_{j=i+1}^{N}  \pi_j T(i \mid j)
}
$$

Clearly, the state visits probability depends on both the one-step transition probability and the prior $\pi_i$. 

For the case of uniform one-step jumps over the lower state $p(i|j) = \dfrac{1}{j-1}$ the expression becomes explicitly dependent on the prior probability of starting at state $k$, $\pi_k$: 

$$
\boxed{p(i) = \pi_i + \dfrac{1}{i}\sum\limits_{j=i+1}^{N}  \pi_j} 
$$

We observe that the distrubution of state vists $p(i)$ depends on the prior probability $\mathbf{\pi}$ for large $i$. We distinguish two cases: 

- $\pi$ vanishs faster than $\dfrac{1}{i}$ the probability follows the prior $p(i) \propto \pi_i$ 
- $\pi$ vanishs slower than $\dfrac{1}{i}$ the probability of visits follows a power law $p(i) \propto \dfrac{1}{i}$.

This result is in agreement with numerical results and previious [work](https://arxiv.org/pdf/1602.05530).  

Taking the example of a uniform prior, $\pi_i=\dfrac{1}{N}$ the distrubution of state visits follows an exact power law $p(i) =\dfrac{1}{i}$. 

$$
\begin{align}
p(i) &= \dfrac{1}{N} + \dfrac{1}{i}\sum\limits_{j=i+1}^{N}  \dfrac{1}{N} \nonumber \\
 &=  \dfrac{1}{N} \left(1 + \dfrac{1}{i}\sum\limits_{j=i+1}^{N}1\right)\nonumber 
\end{align}
$$

Which results in an exact Zipf's law

$$
\boxed{p(i) = \dfrac{1}{i}}
$$

