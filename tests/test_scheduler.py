from core.agents.scheduler import SchedulerAgent


def test_items_per_day_parses_frequency() -> None:
    agent = SchedulerAgent()
    assert agent._items_per_day({"parameters": {"frequency": "2 por dia"}}) == 2
    assert agent._items_per_day({"parameters": {"frequency": "1 por dia"}}) == 1
