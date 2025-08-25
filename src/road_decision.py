from src.const import MAX_SIZE_STACK_ROAD_DECISION, ACTION_DECISION


class RoadDecision:
    @staticmethod
    def decide(road_decision: list[str]) -> str:
        if road_decision.count(ACTION_DECISION[2]) > MAX_SIZE_STACK_ROAD_DECISION // 2:
            return ACTION_DECISION[2]
        return ACTION_DECISION[1]
