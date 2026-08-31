"""Демо-сцени Bug Triage агента: щасливий шлях + типові збої.

Для сцени turns_exhausted запусти окремо з обмеженим лімітом кроків:
  MAX_TURNS=1 python run.py "Хто знайшов баги в релізі R42 і яка їхня причина?"
"""

from core.agent import run_agent, reset_usage
from domain.bug_backend import tools
from config import BASE_PROMPT


def scene(title: str, query: str):
    print(f"\n=== {title} ===")
    print(f"Запит: «{query}»")
    reset_usage()
    result = run_agent(system=BASE_PROMPT, tools=tools(), query=query)
    for step in result.get("trace", []):
        marker = "✗" if step.get("failed") else "✓"
        print(f"  {marker} {step['tool']}({step['input']}) → {step['output']}")
    print(f"Результат (outcome): {result['outcome']}")
    if result["failures"]:
        print(f"Збої інструментів (tool_error): {result['failures']}")
    if result.get("no_tool_used"):
        print("no_tool_used: True (жоден інструмент не викликано)")
    print(f"Відповідь: {result['answer']}")
    return result


if __name__ == "__main__":
    # 1. Щасливий шлях: справжній ланцюжок list → details
    scene("Щасливий шлях (ok)",
          "Хто знайшов баги в релізі R42 і яка їхня причина?")

    # 2. Неіснуючий реліз → tool_error усередині list_release_bugs
    scene("Неіснуючий реліз (tool_error)",
          "Порахуй, скільки RC-багів у релізі R99")

    # 3. Запит не по темі → жоден інструмент не підходить
    scene("Запит не по темі (no_tool_used)",
          "Яка сьогодні погода в Києві?")

    # 4. Баг з невизначеною причиною — перевірка, що агент не вигадує
    scene("Неповні дані (агент не має вигадувати)",
          "Яка причина бага BUG-1080?")