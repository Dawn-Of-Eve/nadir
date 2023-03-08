### Copyright 2023 [Dawn Of Eve]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Dict, Any, Optional
from dataclasses import dataclass

import torch

from .base import BaseOptimizer
from .base import BaseConfig


__all__ = ['LionConfig', 'Lion']

@dataclass
class LionConfig(BaseConfig):
  lr : float = 1E-4
  momentum : bool = True
  beta_1 : float = 0.9
  beta_2 : float = 0.99
  eps : float = 1E-8
  weight_decay : float = 0.



class Lion(BaseOptimizer):
  
  def __init__(self, params, config: LionConfig = LionConfig()):
    if not config.momentum:
      raise ValueError(f"Invalid value for momentum in config: {config.momentum} ", 
                       "Value must be True")
    if not 1 > config.beta_1 > 0.:
      raise ValueError(f"Invalid value for beta_1 in config: {config.beta_1} ", 
                       "Value must be between 1 and 0")
    if not 1 > config.beta_2 > 0.:
      raise ValueError(f"Invalid value for beta_2 in config: {config.beta_2} ", 
                       "Value must be between 1 and 0")
    super().__init__(params, config)
    self.config = config

  def momentum(self, state, grad):
    m = state['momentum']
    beta_1 = self.config.beta_1
    beta_2 = self.config.beta_2

    u = m.mul(beta_1).add_(grad, alpha=(1-beta_1))
    
    m.mul_(beta_2).add_(grad, alpha=(1-beta_2))

    state['momentum'] = m

    return torch.sign(u)