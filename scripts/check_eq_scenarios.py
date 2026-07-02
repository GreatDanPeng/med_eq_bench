#!/usr/bin/env python3
"""Validate EQ scenario dictionaries."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS_PATH = REPO_ROOT / "config" / "eq_scenarios.py"
COLLECTION_NAMES = (
    "TEST_EQ_SCENARIOS",
    "CHOOSING_WISELY_EQ_SCENARIOS",
    "EQ_SCENARIOS",
    "EXTREME_EQ_SCENARIOS",
)
REQUIRED_FIELDS = {
    "scenario_id",
    "interaction_type",
    "patient_profile",
    "physician_profile",
    "clinical_guidelines",
    "gold_standard_action",
}
REQUIRED_PATIENT_FIELDS = {
    "age",
    "gender",
    "chief_complaint",
    "emotional_state",
    "health_anxiety_level",
    "previous_experiences",
}


def constant_key(node: ast.AST) -> object:
    if isinstance(node, ast.Constant) and isinstance(node.value, (str, int, float, bool, type(None))):
        return node.value
    return None


def find_duplicate_literal_keys(tree: ast.AST) -> list[str]:
    issues: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        seen: dict[object, int] = {}
        for key_node in node.keys:
            if key_node is None:
                continue
            key = constant_key(key_node)
            if key is None:
                continue
            line = getattr(key_node, "lineno", getattr(node, "lineno", 0))
            if key in seen:
                issues.append(f"{SCENARIOS_PATH}:{line}: duplicate literal key {key!r}; first seen at line {seen[key]}")
            else:
                seen[key] = line
    return issues


def scenario_collections():
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

    from config.eq_settings import (  # pylint: disable=import-outside-toplevel
        ActionType,
        AnxietyLevel,
        EmotionState,
        GuidelinesType,
        InteractionScenario,
        InteractionType,
        PhysicianProfile,
    )
    import config.eq_scenarios as eq_scenarios  # pylint: disable=import-outside-toplevel

    enum_types = {
        "interaction_type": InteractionType,
        "clinical_guidelines": GuidelinesType,
        "gold_standard_action": ActionType,
    }
    patient_enum_types = {
        "emotional_state": EmotionState,
        "health_anxiety_level": AnxietyLevel,
    }

    return eq_scenarios, InteractionScenario, PhysicianProfile, enum_types, patient_enum_types


def validate_imported_scenarios() -> list[str]:
    issues: list[str] = []
    eq_scenarios, interaction_scenario, physician_profile, enum_types, patient_enum_types = scenario_collections()
    for collection_name in COLLECTION_NAMES:
        collection = getattr(eq_scenarios, collection_name, None)
        if collection is None:
            issues.append(f"missing collection {collection_name}")
            continue
        if not isinstance(collection, dict):
            issues.append(f"{collection_name} is not a dict")
            continue

        inner_ids: dict[str, str] = {}
        for key, scenario in collection.items():
            label = f"{collection_name}.{key}"

            if not isinstance(scenario, dict):
                issues.append(f"{label}: scenario value is not a dict")
                continue

            missing = REQUIRED_FIELDS - scenario.keys()
            if missing:
                issues.append(f"{label}: missing required fields {sorted(missing)}")
                continue

            if scenario["scenario_id"] != key:
                issues.append(f"{label}: inner scenario_id {scenario['scenario_id']!r} does not match dict key")
            if scenario["scenario_id"] in inner_ids:
                issues.append(f"{label}: inner scenario_id duplicates {inner_ids[scenario['scenario_id']]}")
            else:
                inner_ids[scenario["scenario_id"]] = label

            for field, enum_type in enum_types.items():
                if not isinstance(scenario[field], enum_type):
                    issues.append(f"{label}: {field} is not {enum_type.__name__}")

            if not isinstance(scenario["physician_profile"], physician_profile):
                issues.append(f"{label}: physician_profile is not PhysicianProfile")

            patient = scenario["patient_profile"]
            if not isinstance(patient, dict):
                issues.append(f"{label}: patient_profile is not a dict")
                continue

            missing_patient = REQUIRED_PATIENT_FIELDS - patient.keys()
            if missing_patient:
                issues.append(f"{label}: missing patient_profile fields {sorted(missing_patient)}")

            for field, enum_type in patient_enum_types.items():
                if field in patient and not isinstance(patient[field], enum_type):
                    issues.append(f"{label}: patient_profile.{field} is not {enum_type.__name__}")

            try:
                interaction_scenario(
                    scenario_id=scenario["scenario_id"],
                    interaction_type=scenario["interaction_type"],
                    patient_profile=scenario["patient_profile"],
                    physician_profile=scenario["physician_profile"],
                    clinical_guidelines=scenario["clinical_guidelines"],
                    gold_standard_action=scenario["gold_standard_action"],
                )
            except Exception as exc:  # pragma: no cover - diagnostic script
                issues.append(f"{label}: cannot instantiate InteractionScenario: {exc}")

    return issues


def main() -> int:
    tree = ast.parse(SCENARIOS_PATH.read_text(encoding="utf-8"), filename=str(SCENARIOS_PATH))
    issues = find_duplicate_literal_keys(tree)
    issues.extend(validate_imported_scenarios())

    if issues:
        print("EQ scenario validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("EQ scenario validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
