"""Abstract base class for domain configurations.

A domain defines:
- A set of evaluation items (e.g., DeFi protocols) with ground truth scores
- Training/held-out splits
- Scenario templates for training
- System prompts for assessment
- Trap items for adversarial bias probing
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EvalItem:
    """A single item to be evaluated (e.g., a DeFi protocol)."""

    name: str
    description: str
    true_score: int  # Ground truth (0-100)
    category: str  # Type/category for the item
    is_training: bool = True  # Whether this item is in the training set


@dataclass
class Scenario:
    """A training scenario for scenario-based learning."""

    name: str
    description: str
    expected_impact: str  # Description of expected score change


@dataclass
class TrapItem:
    """A trap item for adversarial bias detection."""

    name: str
    description: str
    true_score: int
    bias_type: str  # What kind of bias this trap catches


class Domain(ABC):
    """Abstract domain configuration."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Domain identifier (e.g., 'DeFi:risk-assessment')."""
        ...

    @property
    @abstractmethod
    def category(self) -> str:
        """Top-level category (e.g., 'DeFi')."""
        ...

    @property
    @abstractmethod
    def subcategory(self) -> str:
        """Subcategory (e.g., 'risk-assessment')."""
        ...

    @abstractmethod
    def get_all_items(self) -> list[EvalItem]:
        """Return all evaluation items."""
        ...

    def get_training_items(self) -> list[EvalItem]:
        """Return items used for training."""
        return [item for item in self.get_all_items() if item.is_training]

    def get_held_out_items(self) -> list[EvalItem]:
        """Return items held out from training (for verification)."""
        return [item for item in self.get_all_items() if not item.is_training]

    @abstractmethod
    def get_scenarios(self) -> list[Scenario]:
        """Return training scenarios."""
        ...

    @abstractmethod
    def get_trap_items(self) -> list[TrapItem]:
        """Return trap items for adversarial bias detection."""
        ...

    @abstractmethod
    def get_assessment_system_prompt(self, memory: str = "") -> str:
        """Return the system prompt for item assessment.

        Args:
            memory: Optional accumulated memory or artifact content to inject.
        """
        ...

    @abstractmethod
    def get_assessment_user_prompt(self, item: EvalItem) -> str:
        """Return the user prompt for assessing a specific item."""
        ...

    @abstractmethod
    def get_export_prompt(self, accumulated_memory: list[str]) -> str:
        """Return the prompt for exporting a memory artifact."""
        ...

    @abstractmethod
    def get_scenario_system_prompt(self, memory: str = "") -> str:
        """Return the system prompt for scenario-based learning."""
        ...
