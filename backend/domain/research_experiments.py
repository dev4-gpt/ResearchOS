"""Explicit contracts for optional research engines; no publication by self-report."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class EngineBudget(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    seconds: int = Field(default=120, ge=1, le=3600)
    calls: int = Field(default=16, ge=1, le=100)
    tokens: int = Field(default=200000, ge=256, le=2000000)
    output_tokens: int = Field(default=2048, ge=128, le=8192)
    max_usd: float = Field(default=1.0, gt=0, le=100)
    # Operator-supplied ceiling for the configured provider, NOT a price quote.
    usd_per_million_token_ceiling: float = Field(default=100.0, gt=0)


class ExperimentSpec(BaseModel):
    model_config = ConfigDict(extra='forbid')
    engine: Literal['alphaevolve', 'harness2']
    mode: Literal['demo', 'live'] = 'demo'
    model: str = Field(default='deterministic-fixture', min_length=1, max_length=150)
    seed: int = Field(default=0, ge=0, le=2147483647)
    steps: int = Field(default=1, ge=1, le=10)
    budget: EngineBudget = Field(default_factory=EngineBudget)
    dataset_path: str | None = None
    parent_run: str | None = Field(default=None, pattern=r'^[a-zA-Z0-9_-]{1,100}$')

    @model_validator(mode='after')
    def live_model(self):
        if self.engine == 'harness2' and self.steps != 1:
            raise ValueError('Harness² research adapter supports k=1 only')
        if self.mode == 'live' and self.model == 'deterministic-fixture':
            raise ValueError('Live execution requires an explicit provider model ID')
        return self
