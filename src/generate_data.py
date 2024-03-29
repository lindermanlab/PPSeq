# Import PyTorch modules
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.distributions as dist
import torch.optim as optim

# Plotting stuff
import matplotlib.pyplot as plt

# Some helper utilities
from tqdm.auto import trange
# We'll use a few functions from scipy
from scipy.signal import find_peaks
from scipy.optimize import linear_sum_assignment

def generate_templates(num_channels, len_waveform, num_neurons):
    # Make (semi) random templates
    templates = []
    for k in range(num_neurons):
        center = dist.Uniform(0.0, num_channels).sample()
        width = dist.Uniform(1.0, 1.0 + num_channels / 10.0).sample()
        spatial_factor = torch.exp(-0.5 * (torch.arange(num_channels) - center)**2 / width**2)

        dt = torch.arange(len_waveform)
        period = len_waveform / (dist.Uniform(1.0, 2.0).sample())
        z = (dt - 0.75 * period) / (.25 * period)
        warp = lambda x: -torch.exp(-x) + 1
        window = torch.exp(-0.5 * z**2)
        shape = torch.sin(2 * torch.pi * dt / period)
        temporal_factor = warp(window * shape)

        template = torch.outer(spatial_factor, temporal_factor)
        template /= torch.linalg.norm(template)
        templates.append(template)

    return torch.abs(torch.stack(templates))


def generate(num_timesteps,
             num_channels,
             len_waveform,
             num_neurons,
             mean_amplitude=15,
             shape_amplitude=3.0,
             noise_std=1,
             sample_freq=1000):
    """Create a random set of model parameters and sample data.

    Parameters:
    num_timesteps: integer number of time samples in the data
    num_channels: integer number of channels
    len_waveform: integer duration (number of samples) of each template
    num_neurons: integer number of neurons
    """
    # Make semi-random templates
    templates = generate_templates(num_channels, len_waveform, num_neurons)

    # Make random amplitudes
    amplitudes = torch.zeros((num_neurons, num_timesteps))
    for k in range(num_neurons):
        num_spikes = dist.Poisson(num_timesteps / sample_freq * 10.0).sample()
        sample_shape = (1 + int(num_spikes),)
        times = dist.Categorical(torch.ones(num_timesteps) / num_timesteps).sample(sample_shape)
        amps = dist.Gamma(shape_amplitude, shape_amplitude / mean_amplitude).sample(sample_shape)
        amplitudes[k, times] = amps

        # Only keep spikes separated by at least D
        times, props = find_peaks(amplitudes[k], distance=len_waveform, height=1e-3)
        amplitudes[k] = 0
        amplitudes[k, times] = torch.tensor(props['peak_heights'], dtype=torch.float32)

    amplitudes = torch.abs(amplitudes)

    # Convolve the signal with each row of the multi-channel template
    #data = F.conv1d(amplitudes.unsqueeze(0),
    #               templates.permute(1, 0, 2).flip(dims=(2,)),
    #               padding=len_waveform-1)[0, :, :-(len_waveform-1)]

    #data += dist.Normal(0.0, noise_std).sample(data.shape)
    true_a = amplitudes
    true_w = templates
    true_b = torch.rand(N) + 0.2
    lambdas = true_b.view(N,1) + F.conv1d(true_a, torch.flip(true_w.permute(1,0,2),[2]), padding=D-1)[:,:-D+1]
    data = torch.poisson(lambdas)

    return templates, amplitudes, true_b, data

def generate_data(N=8, T=2000, K=5, D=10):
  """
  -X: (N, T)
  """

  true_w = torch.linspace(10, 0, D).repeat(K,N,1)
  true_a = torch.rand((K,T)) * 10
  true_b = torch.rand(N) *10
  lambdas = true_b.view(N,1) + F.conv1d(true_a, torch.flip(true_w.permute(1,0,2),[2]), padding=D-1)[:,:-D+1]
  X = torch.poisson(lambdas)
  return X, true_b, true_a, true_w

  