"""Expert agent training — 20-round curriculum.

Phase 1 (Rounds 1-5): Basic assessment with calibration feedback
Phase 2 (Rounds 6-10): Scenario-based learning
Phase 3 (Rounds 11-20): Reassessment with accumulated experience
"""

from ..api import call_api_json
from ..config import MODEL, MAX_TOKENS_ASSESSMENT, MAX_TOKENS_SCENARIO
from ..domains.base import Domain


def train_expert(
    client,
    domain: Domain,
    model: str = MODEL,
) -> list[str]:
    """Train an expert agent over N rounds (default 20).

    Returns accumulated_memory: a list of learning strings from each round.
    """
    accumulated_memory = []
    training_items = domain.get_training_items()
    scenarios = domain.get_scenarios()
    total_rounds = domain.training_rounds
    phase1_end = max(1, total_rounds // 4)  # first 25% for calibration
    num_scenarios = min(len(scenarios), 5)
    phase3_start = phase1_end + num_scenarios + 1

    # Phase 1: Basic assessment (rounds 1 to phase1_end)
    for round_num in range(1, phase1_end + 1):
        item = training_items[(round_num - 1) % len(training_items)]
        memory_text = "\n".join(accumulated_memory) if accumulated_memory else ""

        result = call_api_json(
            client=client,
            system=domain.get_assessment_system_prompt(memory=memory_text),
            user_message=domain.get_assessment_user_prompt(item),
            max_tokens=MAX_TOKENS_ASSESSMENT,
            model=model,
            default_on_failure={
                "score": 50,
                "reasoning": "Failed to parse response",
                "red_flags": [],
                "confidence": "low",
            },
        )

        score = result.get("score", 50)
        error = abs(score - item.true_score)

        feedback = (
            f"Round {round_num} — {item.name}: "
            f"Your score: {score}, True score: {item.true_score}, "
            f"Error: {error}. "
        )
        if error <= 10:
            feedback += "Good calibration. "
        elif error <= 25:
            feedback += "Moderate error. "
        else:
            feedback += "Significant miscalibration. "

        if item.risk_factors:
            feedback += f"Key risk factors you should note: {', '.join(item.risk_factors)}. "
        if item.mitigants:
            feedback += f"Key mitigants: {', '.join(item.mitigants)}."

        accumulated_memory.append(feedback)

    # Phase 2: Scenario-based learning
    for i, scenario in enumerate(scenarios[:num_scenarios]):
        memory_text = "\n".join(accumulated_memory)

        result = call_api_json(
            client=client,
            system=domain.get_scenario_system_prompt(memory=memory_text),
            user_message=scenario.description,
            max_tokens=MAX_TOKENS_SCENARIO,
            model=model,
            default_on_failure={
                "original_score": 50,
                "updated_score": 50,
                "reasoning": "Failed to parse",
                "lesson": "N/A",
            },
        )

        # Use ground truth lesson if available, otherwise fall back to LLM's extraction
        lesson = scenario.lesson if scenario.lesson else result.get("lesson", "No lesson extracted")
        accumulated_memory.append(
            f"Scenario {i + 1} ({scenario.name}): {lesson}"
        )

    # Phase 3: Reassessment (rounds phase3_start to total_rounds)
    for round_num in range(phase3_start, total_rounds + 1):
        item = training_items[(round_num - phase3_start) % len(training_items)]
        memory_text = "\n".join(accumulated_memory)

        result = call_api_json(
            client=client,
            system=domain.get_assessment_system_prompt(memory=memory_text),
            user_message=domain.get_assessment_user_prompt(item),
            max_tokens=MAX_TOKENS_ASSESSMENT,
            model=model,
            default_on_failure={
                "score": 50,
                "reasoning": "Failed to parse response",
                "red_flags": [],
                "confidence": "low",
            },
        )

        score = result.get("score", 50)
        error = abs(score - item.true_score)

        if error <= 3:
            feedback = f"Round {round_num} — {item.name}: Score {score} (true: {item.true_score}). Improved — excellent calibration."
        elif score > item.true_score:
            feedback = f"Round {round_num} — {item.name}: Score {score} (true: {item.true_score}). Still too high by {error}."
        else:
            feedback = f"Round {round_num} — {item.name}: Score {score} (true: {item.true_score}). Still too low by {error}."

        accumulated_memory.append(feedback)

    return accumulated_memory
