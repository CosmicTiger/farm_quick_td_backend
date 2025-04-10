from datetime import UTC, datetime

date_test = datetime.now(tz=UTC).isoformat()

TEST_TASK_1 = {
    "title": "🗄️ Backend - E2E Test Task A",
    "description": "This is a test task for E2E testing from Backend.",
    "status": 0,
    "priority": 0,
    "sub_tasks": [],
    "due_date": date_test,
    "assigned_to": None,
}

TEST_TASK_2 = {
    "title": "🗄️ Backend - E2E Test Task B",
    "description": (
        "This is a secondary test task for E2E testing from Backend. "
        "For test assignment of user and subtasks relationships"
    ),
    "status": 0,
    "priority": 0,
    "sub_tasks": [
        {
            "id": "",
            "title": "",
            "description": "",
            "due_date": "",
            "relation_type": "relates_to",
        },
    ],
    "due_date": date_test,
    "assigned_to": None,
}
