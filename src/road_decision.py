from src.const import MAX_SIZE_STACK_ROAD_DECISION, ACTION_DECISION
from src.pico_script.pico_controller import PicoController


class RoadDecision:
    @staticmethod
    def decide(road_decision: list[str]) -> str:
        if road_decision.count(ACTION_DECISION[2]) > MAX_SIZE_STACK_ROAD_DECISION // 2:
            return ACTION_DECISION[2]
        if road_decision.count(ACTION_DECISION[3]) > MAX_SIZE_STACK_ROAD_DECISION // 2:
            return ACTION_DECISION[3]
        if road_decision.count(ACTION_DECISION[0]) > MAX_SIZE_STACK_ROAD_DECISION // 2:
            return ACTION_DECISION[0]
        return ACTION_DECISION[1]

    @staticmethod
    def execute_action(action: str):
        if action in (ACTION_DECISION[2], ACTION_DECISION[3]):
            PicoController.active_buzzer()
