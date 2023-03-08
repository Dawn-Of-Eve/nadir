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


__all__ = ['AdamWConfig', 'AdamW']

@dataclass
class AdamWConfig(BaseConfig):
  lr : float = 3E-4
  momentum : bool = True
  adaptive : bool = True
  beta_1 : float = 0.9
  beta_2 : float = 0.999
  eps : float = 1E-8
  weight_decay : float = 0.01

class AdamW(BaseOptimizer):
  def __init__ (self, params, config : AdamWConfig = AdamWConfig()):
    if not config.momentum:
      raise ValueError(f"Invalid value for momentum in config: {config.momentum} ", 
                       "Value must be True")
    if not config.adaptive:
      raise ValueError(f"Invalid value for adaptive in config: {config.adaptive} ", 
                       "Value must be True")
    if not 1.0 > config.weight_decay > 0.0:
      raise ValueError(f"Invalid value for weight_decay in config: {config.weight_decay} ", 
                       "Value must be float between 0 and 1")  
    super().__init__(params, config)
    
    self.config = config