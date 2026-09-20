import main


def test_extract_entities_finds_capitalized_names():
    text = "Follow up with Alice and Bob about the firmware project"
    entities = main.extract_entities(text)

    entity_values = [e["value"] for e in entities]
    assert "Alice" in entity_values
    assert "Bob" in entity_values


def test_extract_entities_finds_acronyms():
    text = "Need to review the GSP PCBA flashing process for W1-1873"
    entities = main.extract_entities(text)

    entity_values = [e["value"] for e in entities]
    assert "GSP" in entity_values
    assert "PCBA" in entity_values
    # W1-1873 is not captured by our simple regex; that's ok for now
    # This test validates that acronyms are captured


def test_extract_themes_finds_firmware_theme():
    text = "Need to fix firmware flashing issues on the board"
    themes = main.extract_themes(text)

    theme_values = [t["value"] for t in themes]
    assert "firmware" in theme_values
    assert "hardware" in theme_values


def test_extract_themes_finds_multiple_themes():
    text = "Deployment delayed. Customer reports firmware failures in field. Needs engineering review by next week."
    themes = main.extract_themes(text)

    theme_values = [t["value"] for t in themes]
    assert "deployment" in theme_values
    assert "firmware" in theme_values
    assert "engineering" in theme_values
    assert "scheduling" in theme_values


def test_extract_tasks_includes_entities_and_themes():
    text = "TODO: Follow up with Alice about the firmware testing failures"
    tasks = main.extract_tasks(text)

    assert len(tasks) == 1
    task = tasks[0]
    assert "Alice" in [e["value"] for e in task["entities"]]
    assert "firmware" in [t["value"] for t in task["themes"]]
    assert "testing" in [t["value"] for t in task["themes"]]


def test_task_structure_includes_provenance_fields():
    text = "Next: review GSP PCBA documentation before deployment"
    tasks = main.extract_tasks(text)

    assert len(tasks) == 1
    task = tasks[0]
    assert "text" in task
    assert "status" in task
    assert "entities" in task
    assert "themes" in task
    assert task["status"] == "pending"
    assert isinstance(task["entities"], list)
    assert isinstance(task["themes"], list)
