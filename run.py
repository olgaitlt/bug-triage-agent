"""Точка входу: один наскрізний прогін Bug Triage агента.

Використання:
  python run.py                       # тестовий запит з config.py
  python run.py "твій запит тут"      # свій запит
"""

import sys
from core.agent import run_agent, USAGE, reset_usage
from domain.bug_backend import tools
from config import BASE_PROMPT, USER_QUERY


def run(query: str) -> dict:
    return run_agent(system=BASE_PROMPT, tools=tools(), query=query)


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or USER_QUERY
    reset_usage()
    result = run(query)

    print(f"Запит: «{query}»\n")

    for step in result.get("trace", []):
        marker = "✗" if step.get("failed") else "✓"
        print(f"  {marker} {step['tool']}({step['input']}) → {step['output']}")

    print(f"\nРезультат (outcome): {result['outcome']}")
    print(f"Відповідь:\n{result['answer']}")

    if USAGE["calls"]:
        print(f"\nТокенів: {USAGE['in']}→{USAGE['out']} за {USAGE['calls']} виклик(и/ів)")
