# Court Simulation 🔬 
------------
This is a agent based simulation supporting Aragon's research towards a decentralized oracle for dispute resolution.

The model will instantiate a number of Jurors with some amount of initial tokens.

For each dispute the ***true*** result will be determined by the model, and each agent will produce an individual ***belief***. Jurors activate each of their ***whole*** tokens for each dispute, and tokens are drawn by the scheduler randomly.

Each Juror will vote honestly with each of their tokens which have been drawn in the current step based on their belief. If the result does not align with global truth then the dispute will be appealed, and the model will select additional tokens until all tokens have participated in the dispute, or the verdict aligns with the truth.

In this model we assume that all agents act honestly and we assume that the agents estimation is normally distributed around the truth. By itself this is not a particularly useful model, but it is intended to provide a baseline representation of the court mechanism, which can be extended to study the dynamics of agents based on various more complex and realistic assumptions.

## Getting Started

### Python
------------
Make sure you have Python 3

### Install Mesa
------------
Install Mesa on Python 3:

    $ pip3 install mesa

### Dependencies
------------
Install all dependencies either manually or by using
```
$ pip3 install -r requirements.txt
```

### Run
------------
Download this repository.
cd into the main directory for this repository.
And run
```
$ python3 run.py
```

### View
------------
The server should host it on [http://127.0.0.1:8521/]()

In the main screen you will see:

- A top bar menu, with flow controls to the right.
- Some parameter sliders:
  - Number of jurors included in the model.
  - Belief threshold: Agents must sample within this many standard deviations from the true value to be coherent.
  - Number of tokens in supply, tokens are split evenly among jurors at initialization.
  - Dispensation percentage: Percentage of activated tokens which are redistributed from incoherent jurors to coherent. See [here](https://docs.google.com/document/d/12fsgREpfxkNgpFYpIOmHh2jkWoFM4siH_fQ2ppU-Uak/edit#) for a reference.
- A main chart showing the amount of disputes, split in `susccessful` and `failed`.
- Another chart showing the resulting [Gini coefficient](https://en.wikipedia.org/wiki/Gini_coefficient) for the inequality distribution of tokens after each dispute.
