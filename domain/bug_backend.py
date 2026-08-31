"""
Фейковий бекенд QA-аналітики. Детермінований, як приклад курсу з посилками.

Реліз R42 — суміш різних причин і джерел виявлення багів (з твоїх реальних
метрик: root cause categories, found_by), плюс один тікет із неповними
даними (root_cause=None) — щоб перевірити, що агент не вигадує причину,
а чесно каже "не визначено".
"""

BUGS = {
    "BUG-1042": {
        "release": "R42", "title": "500 error on checkout",
        "component": "checkout-service",
        "root_cause": "Unhandled Exceptions (Sentry / 500s)",
        "found_by": "Support", "is_rc": False, "is_hotfix": True,
    },
    "BUG-1055": {
        "release": "R42", "title": "Wrong price after coupon applied",
        "component": "pricing-service",
        "root_cause": "Coding Error / Logic Defect",
        "found_by": "QA", "is_rc": True, "is_hotfix": False,
    },
    "BUG-1061": {
        "release": "R42", "title": "Timeout on report export",
        "component": "reporting-service",
        "root_cause": "Performance / Timeout / Load",
        "found_by": "Client", "is_rc": False, "is_hotfix": False,
    },
    "BUG-1073": {
        "release": "R42", "title": "Failed deploy after merge conflict",
        "component": "ci-pipeline",
        "root_cause": "Merge/Rebase Issue",
        "found_by": "Developer", "is_rc": True, "is_hotfix": False,
    },
    "BUG-1080": {
        "release": "R42", "title": "Unexplained crash on report screen",
        "component": "reporting-service",
        "root_cause": None,          # причина ще не встановлена — навмисно
        "found_by": "AQA", "is_rc": True, "is_hotfix": False,
    },
    "BUG-2001": {
        "release": "R41", "title": "Permission bypass on admin panel",
        "component": "auth-service",
        "root_cause": "Security / Permission Logic",
        "found_by": "Release QC", "is_rc": True, "is_hotfix": True,
    },
}


# ── інструменти ───────────────────────────────────────────────
def list_release_bugs(release: str) -> dict:
    ids = [bid for bid, b in BUGS.items() if b["release"] == release.strip().upper()]
    if not ids:
        return {"error": "not_found", "release": release,
                "hint": "Перевірте номер релізу, напр. R42."}
    return {"release": release, "bug_ids": ids, "count": len(ids)}


def get_bug_details(bug_id: str) -> dict:
    b = BUGS.get(bug_id.strip().upper())
    if not b:
        return {"error": "not_found", "bug_id": bug_id,
                "hint": "Перевірте ID бага — можливо, його не існує в цьому релізі."}
    return b


IMPL = {
    "list_release_bugs": list_release_bugs,
    "get_bug_details": get_bug_details,
}


def dispatch(name: str, args: dict) -> dict:
    fn = IMPL.get(name)
    if not fn:
        return {"error": f"unknown_tool:{name}"}
    try:
        return fn(**args)
    except TypeError as e:
        return {"error": f"bad_args: {e}"}


# ── схеми ─────────────────────────────────────────────────────
def _schema(name, desc, props, required):
    return {"name": name, "description": desc,
            "input_schema": {"type": "object", "properties": props, "required": required}}


TOOL_SCHEMAS = {
    "list_release_bugs": _schema(
        "list_release_bugs",
        "Повертає список ID багів для вказаного релізу (напр. R42). "
        "Викликай ПЕРШИМ, щоб дізнатись, які тікети взагалі є в релізі.",
        {"release": {"type": "string", "description": "Код релізу, напр. R42"}},
        ["release"]),
    "get_bug_details": _schema(
        "get_bug_details",
        "Повертає повні деталі одного бага за його ID: root cause, хто знайшов, "
        "чи це RC-баг, чи hotfix. Викликай ПІСЛЯ list_release_bugs — для кожного "
        "ID зі списку, який тебе цікавить.",
        {"bug_id": {"type": "string", "description": "ID бага, напр. BUG-1042"}},
        ["bug_id"]),
}


def tools() -> list:
    return [TOOL_SCHEMAS["list_release_bugs"], TOOL_SCHEMAS["get_bug_details"]]
