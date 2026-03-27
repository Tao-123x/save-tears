from pathlib import Path
import runpy


GENERATOR_PATH = Path("/Users/tanxuebin/Downloads/up-clean/tmp/docs/generate_requirement_form_templates.py")

EXPECTED_GROUPS = [
    {
        "key": "water_treatment",
        "zh_filename": "水处理组需求采集表.docx",
        "en_filename": "Water_Treatment_Group_Requirement_Form.docx",
        "zh_title": "水处理组需求采集表",
        "en_title": "Water Treatment Group Requirement Collection Form",
    },
    {
        "key": "drainage",
        "zh_filename": "排水组需求采集表.docx",
        "en_filename": "Drainage_Group_Requirement_Form.docx",
        "zh_title": "排水组需求采集表",
        "en_title": "Drainage Group Requirement Collection Form",
    },
    {
        "key": "application",
        "zh_filename": "应用组需求采集表.docx",
        "en_filename": "Application_Group_Requirement_Form.docx",
        "zh_title": "应用组需求采集表",
        "en_title": "Application Group Requirement Collection Form",
    },
    {
        "key": "derection",
        "zh_filename": "Derection组需求采集表.docx",
        "en_filename": "Derection_Group_Requirement_Form.docx",
        "zh_title": "Derection组需求采集表",
        "en_title": "Derection Group Requirement Collection Form",
    },
]


def main():
    namespace = runpy.run_path(str(GENERATOR_PATH))
    groups = namespace.get("GROUPS")
    part_a_fields = namespace.get("PART_A_FIELDS")
    part_b_headers = namespace.get("PART_B_HEADERS")

    if not isinstance(groups, list):
        raise ValueError(f"GROUPS must be a list, got {type(groups).__name__}")
    if not isinstance(part_a_fields, list):
        raise ValueError(f"PART_A_FIELDS must be a list, got {type(part_a_fields).__name__}")
    if not isinstance(part_b_headers, list):
        raise ValueError(f"PART_B_HEADERS must be a list, got {type(part_b_headers).__name__}")

    if len(groups) != 4:
        raise ValueError(f"Expected 4 groups, got {len(groups)}")
    if len(part_a_fields) != 8:
        raise ValueError(f"Expected 8 Part A fields, got {len(part_a_fields)}")
    if len(part_b_headers) != 11:
        raise ValueError(f"Expected 11 Part B headers, got {len(part_b_headers)}")

    required_keys = {
        "key",
        "zh_filename",
        "en_filename",
        "zh_title",
        "en_title",
        "zh_hints",
        "en_hints",
    }

    seen_keys = set()
    seen_zh_filenames = set()
    seen_en_filenames = set()
    seen_zh_titles = set()
    seen_en_titles = set()

    for index, group in enumerate(groups):
        if not isinstance(group, dict):
            raise ValueError(f"Group at index {index} must be a dict, got {type(group).__name__}")

        missing = required_keys - set(group)
        if missing:
            raise ValueError(f"Missing keys for {group.get('key')}: {sorted(missing)}")

        expected = EXPECTED_GROUPS[index]
        for field in ("key", "zh_filename", "en_filename", "zh_title", "en_title"):
            if group[field] != expected[field]:
                raise ValueError(
                    f"Unexpected {field} for group at index {index}: "
                    f"expected {expected[field]!r}, got {group[field]!r}"
                )

        if not isinstance(group["zh_hints"], list):
            raise ValueError(f"Chinese hints for {group['key']} must be a list")
        if not isinstance(group["en_hints"], list):
            raise ValueError(f"English hints for {group['key']} must be a list")

        if len(group["zh_hints"]) < 3:
            raise ValueError(f"Chinese hints too short for {group['key']}")
        if len(group["en_hints"]) < 3:
            raise ValueError(f"English hints too short for {group['key']}")

        for hint_index, hint in enumerate(group["zh_hints"]):
            if not isinstance(hint, str):
                raise ValueError(
                    f"Chinese hint {hint_index} for {group['key']} must be a string, got {type(hint).__name__}"
                )
        for hint_index, hint in enumerate(group["en_hints"]):
            if not isinstance(hint, str):
                raise ValueError(
                    f"English hint {hint_index} for {group['key']} must be a string, got {type(hint).__name__}"
                )

        if group["key"] in seen_keys:
            raise ValueError(f"Duplicate group key: {group['key']}")
        if group["zh_filename"] in seen_zh_filenames:
            raise ValueError(f"Duplicate Chinese filename: {group['zh_filename']}")
        if group["en_filename"] in seen_en_filenames:
            raise ValueError(f"Duplicate English filename: {group['en_filename']}")
        if group["zh_title"] in seen_zh_titles:
            raise ValueError(f"Duplicate Chinese title: {group['zh_title']}")
        if group["en_title"] in seen_en_titles:
            raise ValueError(f"Duplicate English title: {group['en_title']}")

        seen_keys.add(group["key"])
        seen_zh_filenames.add(group["zh_filename"])
        seen_en_filenames.add(group["en_filename"])
        seen_zh_titles.add(group["zh_title"])
        seen_en_titles.add(group["en_title"])

    print("PASS: content schema is complete")


if __name__ == "__main__":
    main()
