import os

from groq import Groq


def main():
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    policy = """
    Sick Leave Policy

    All employees are eligible for sick leave.

    Employees receive 10 days of sick leave annually.

    Employees must inform their manager on the first day of absence.
    """

    prompt = f"""
    Read the following company policy carefully.

    POLICY:
    {policy}

    TASK:
    Extract the following information:
    1. Number of sick leave days.
    2. Employee eligibility.
    3. Reporting process.

    Return the answer as valid JSON:
    {{
        "sick_leave_days": "",
        "eligibility": "",
        "reporting_process": ""
    }}

    Do not invent information. If something is missing,
    write "Not specified".
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    print("GROQ MODEL RESPONSE:")
    print(response.choices[0].message.content)

    print("\nTOKEN USAGE:")
    print(response.usage)


if __name__ == "__main__":
    main()
