# PP-Seq in PyTorch

This repo implements the point process model of neural sequences (PP-Seq) in PyTorch.  The original model is described in:

> [Alex H. Williams](https://alexhwilliams.info) :coffee:, [Anthony Degleris](https://degleris1.github.io/) :sunrise_over_mountains:, [Yixin Wang](http://people.eecs.berkeley.edu/~ywang/), [Scott W. Linderman](https://web.stanford.edu/~swl1/) :loudspeaker:.
> <br>[Point process models for sequence detection in high-dimensional neural spike trains](https://arxiv.org/abs/2010.04875).
> <br> *Neural Information Processing Systems 2020*, Vancouver, CA.

Here, we implement a simpler inference algorithm that works in discrete time, and a PyTorch implementation takes advantage of parallelization across time bins using a GPU.

This model aims to identify sequential firing patterns in neural spike trains in an unsupervised manner.
For example, consider the spike train below<sup>(1)</sup>:

![image](https://user-images.githubusercontent.com/636625/94763493-36bc0400-035f-11eb-95b7-40f583ed599b.png)

By eye, we see no obvious structure in these data. However, by re-ordering the neurons according to PP-Seq's inferred sequences, we obtain:

![image](https://user-images.githubusercontent.com/636625/94767663-ee521580-0361-11eb-8729-de9eee1ab7d9.png)

Further, the model provides (probabilistic) assignment labels to each spike. In this case, we fit a model with two types of sequences. Below we use the model to color each spike as red (sequence 1), blue (sequence 2), or black (non-sequence background spike):

![image](https://user-images.githubusercontent.com/636625/94767637-db3f4580-0361-11eb-89dd-28fd8a25c468.png)

**Footnote.** (1) These data are deconvolved spikes from a calcium imaging recording from zebra finch HVC. These data were published in [Mackevicius*, Bahle*, et al. (2019)](https://elifesciences.org/articles/38471) and are freely available online at https://github.com/FeeLab/seqNMF.

