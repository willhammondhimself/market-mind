"""Base agent interface. All AI agents must implement this."""
from __future__ import annotations

from abc import ABC, abstractmethod

from server.types import AgentAction, AgentObservation, SessionConfig, SessionResult


class BaseAgent(ABC):
    """Abstract base class for all AI agents in MarketMind.

    Every agent — rule-based, RL, evolutionary, or LLM — implements this
    interface. The matching engine calls on_tick() every 50ms to get the
    agent's desired actions.
    """

    def __init__(self, agent_id: str, agent_type: str) -> None:
        self.agent_id = agent_id
        self.agent_type = agent_type

    @abstractmethod
    async def on_tick(self, observation: AgentObservation) -> list[AgentAction]:
        """Called each tick (50ms). Return zero or more actions.

        Args:
            observation: Current market state visible to this agent.

        Returns:
            List of actions (place_order, cancel_order, modify_order).
        """
        ...

    @abstractmethod
    async def on_session_start(self, config: SessionConfig) -> None:
        """Called when session begins. Initialize agent state here.

        Args:
            config: Session configuration (mode, assets, duration, etc.).
        """
        ...

    @abstractmethod
    async def on_session_end(self, result: SessionResult) -> None:
        """Called when session ends. Update models or log results here.

        Args:
            result: Final session outcome.
        """
        ...
