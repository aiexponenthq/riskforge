"""PluginRegistry — discovers and caches all entry_point-registered plugins."""

from __future__ import annotations

import importlib.metadata


class PluginNotFoundError(KeyError):
    pass


class PluginRegistry:
    """Discovers and caches all entry_point-registered plugins.

    Groups:
      riskforge.exporters      -> Exporter implementations
      riskforge.adapters       -> IntegrationAdapter implementations
      riskforge.question_banks -> Question bank classes
    """

    _GROUPS = {
        "exporters": "riskforge.exporters",
        "adapters": "riskforge.adapters",
        "question_banks": "riskforge.question_banks",
    }

    def __init__(self) -> None:
        self._exporters: dict[str, type] = {}
        self._adapters: dict[str, type] = {}
        self._question_banks: dict[str, object] = {}

    def load_all(self) -> None:
        for ep in importlib.metadata.entry_points(group=self._GROUPS["exporters"]):
            self._exporters[ep.name] = ep.load()
        for ep in importlib.metadata.entry_points(group=self._GROUPS["adapters"]):
            self._adapters[ep.name] = ep.load()
        for ep in importlib.metadata.entry_points(group=self._GROUPS["question_banks"]):
            self._question_banks[ep.name] = ep.load()

    def get_exporter(self, name: str):
        cls = self._exporters.get(name)
        if cls is None:
            raise PluginNotFoundError(
                f"No exporter registered for format '{name}'. Available: {list(self._exporters)}"
            )
        return cls()

    def get_adapter(self, name: str):
        cls = self._adapters.get(name)
        if cls is None:
            raise PluginNotFoundError(
                f"No adapter registered for source '{name}'. Available: {list(self._adapters)}"
            )
        return cls()

    def list_exporters(self) -> list[str]:
        return list(self._exporters)

    def list_adapters(self) -> list[str]:
        return list(self._adapters)

    def list_question_banks(self) -> list[str]:
        return list(self._question_banks)
