import csv
import re
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
POLICY_DIR = BASE_DIR / "data" / "policies"
RESULTS_DIR = BASE_DIR / "results"

POLICY_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# 20 synthetic policy documents
policies = [
    (
        "annual_leave",
        "Annual Leave Policy",
        "All full-time employees are eligible for annual leave.",
        "Employees receive 20 days of annual leave each year.",
        "Employees must submit leave requests 5 days in advance. Managers approve requests.",
    ),
    (
        "sick_leave",
        "Sick Leave Policy",
        "All employees are eligible for sick leave.",
        "Employees receive 10 days of sick leave annually.",
        "Employees must inform their manager on the first day of absence.",
    ),
    (
        "casual_leave",
        "Casual Leave Policy",
        "All permanent employees are eligible for casual leave.",
        "Employees receive 6 days of casual leave annually.",
        "Requests should be submitted at least 2 days in advance.",
    ),
    (
        "attendance",
        "Attendance Policy",
        "All employees must record their attendance.",
        "The standard working hours are 9 AM to 6 PM.",
        "Employees must report late arrivals to their manager.",
    ),
    (
        "remote_work",
        "Remote Work Policy",
        "Employees with manager approval can work remotely.",
        "Employees can work from home up to 2 days per week.",
        "Remote work requests must be submitted one day in advance.",
    ),
    (
        "overtime",
        "Overtime Policy",
        "Employees asked to work beyond regular hours are eligible.",
        "Overtime must be approved by the department manager.",
        "Employees must record overtime hours in the attendance system.",
    ),
    (
        "travel",
        "Business Travel Policy",
        "Employees travelling for official business are eligible.",
        "Travel expenses must follow the company-approved budget.",
        "Employees must obtain manager approval before booking tickets.",
    ),
    (
        "expenses",
        "Expense Reimbursement Policy",
        "Employees spending money on approved business activities are eligible.",
        "Valid expenses are reimbursed within 15 working days.",
        "Employees must submit receipts and an expense claim form.",
    ),
    (
        "laptop",
        "Laptop Usage Policy",
        "Company laptops are provided to authorized employees.",
        "Laptops must be used primarily for official work.",
        "Employees must report damaged or lost laptops to IT immediately.",
    ),
    (
        "password",
        "Password Security Policy",
        "All employees with company accounts must follow this policy.",
        "Passwords must contain at least 12 characters.",
        "Employees must never share passwords with other people.",
    ),
    (
        "data_privacy",
        "Data Privacy Policy",
        "All employees handling company or customer data must comply.",
        "Confidential customer data must be protected from unauthorized access.",
        "Employees must report suspected data breaches to the security team immediately.",
    ),
    (
        "id_card",
        "Employee ID Card Policy",
        "Every employee receives a company ID card.",
        "Employees must wear their ID card inside company premises.",
        "Lost ID cards must be reported to HR within 24 hours.",
    ),
    (
        "visitor",
        "Visitor Policy",
        "All visitors must follow company security procedures.",
        "Visitors must register at the reception desk.",
        "Employees must accompany visitors inside restricted areas.",
    ),
    (
        "email",
        "Email Usage Policy",
        "All employees using company email accounts must comply.",
        "Company email should be used for professional communication.",
        "Employees must not open suspicious email attachments.",
    ),
    (
        "internet",
        "Internet Usage Policy",
        "All employees using company internet must follow this policy.",
        "Internet access should primarily support business activities.",
        "Employees must not download unauthorized software.",
    ),
    (
        "performance",
        "Performance Review Policy",
        "All regular employees participate in performance reviews.",
        "Performance reviews are conducted twice a year.",
        "Managers discuss goals and feedback during review meetings.",
    ),
    (
        "training",
        "Employee Training Policy",
        "All employees can participate in approved training programs.",
        "Employees receive an annual training budget of 10000 rupees.",
        "Training requests must be approved by the reporting manager.",
    ),
    (
        "grievance",
        "Employee Grievance Policy",
        "All employees can raise workplace concerns.",
        "HR reviews submitted grievances within 7 working days.",
        "Employees can submit grievances through the HR portal.",
    ),
    (
        "resignation",
        "Resignation Policy",
        "All employees wishing to leave the company must follow this policy.",
        "Employees must provide 30 days of notice.",
        "Resignation requests must be submitted to the reporting manager.",
    ),
    (
        "refund",
        "Customer Refund Policy",
        "Customers who meet the refund conditions are eligible.",
        "Approved refunds are processed within 7 business days.",
        "Customers must submit proof of purchase and a refund request.",
    ),
]


def create_documents():
    """Create 20 synthetic policy text files."""

    for slug, title, eligibility, rule, procedure in policies:
        content = f"""{title}

{eligibility}

{rule}

{procedure}
"""

        file_path = POLICY_DIR / f"{slug}.txt"
        file_path.write_text(content, encoding="utf-8")

    print(f"Created {len(policies)} policy documents.")


# Read all policy documents
def load_documents():
    documents = []

    for file_path in sorted(POLICY_DIR.glob("*.txt")):
        documents.append(
            {
                "source": file_path.name,
                "text": file_path.read_text(encoding="utf-8"),
            }
        )

    return documents


# Method 1: Fixed-size character chunking
def fixed_size_chunk(text, chunk_size=200, overlap=30):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        if end >= len(text):
            break

        start = end - overlap

    return chunks


# Method 2: Paragraph-based chunking
def paragraph_chunk(text):
    return [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]


# Method 3: Sentence-based chunking
def sentence_chunk(text, sentences_per_chunk=2):
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    chunks = []

    for index in range(0, len(sentences), sentences_per_chunk):
        group = sentences[index : index + sentences_per_chunk]
        chunks.append(" ".join(group))

    return chunks


def save_chunks(all_chunks, filename):
    """Save chunks and their source documents to CSV."""

    output_path = RESULTS_DIR / filename

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["source", "chunk_id", "text"],
        )

        writer.writeheader()
        writer.writerows(all_chunks)


def main():
    # Create the 20 documents
    create_documents()

    # Load documents
    documents = load_documents()

    methods = {
        "fixed": fixed_size_chunk,
        "paragraph": paragraph_chunk,
        "sentence": sentence_chunk,
    }

    for method_name, chunk_function in methods.items():
        all_chunks = []

        for document in documents:
            chunks = chunk_function(document["text"])

            for index, chunk in enumerate(chunks):
                all_chunks.append(
                    {
                        "source": document["source"],
                        "chunk_id": index,
                        "text": chunk,
                    }
                )

        output_file = f"chunks_{method_name}.csv"
        save_chunks(all_chunks, output_file)

        print(f"{method_name}: {len(all_chunks)} chunks saved to {output_file}")


if __name__ == "__main__":
    main()
