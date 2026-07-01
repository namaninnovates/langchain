"""
AI-Powered College Assistant using LangChain Tool Calling Agent
===============================================================
Automatically identifies user requests and invokes the appropriate tool(s)
to provide accurate responses for college-related queries.

Tools:
  1. Attendance Calculator
  2. Result Calculator
  3. Fee Balance Calculator
  4. Library Fine Calculator
  5. Hostel Fee Calculator
  6. Student Information Tool (Bonus)
"""

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI

# ──────────────────────────────────────────────────────────────
# Tool 1: Attendance Calculator
# ──────────────────────────────────────────────────────────────
@tool
def attendance_calculator(total_classes: int, attended_classes: int) -> str:
    """Calculate student attendance percentage and determine exam eligibility.
    Use this tool when the user asks about attendance, exam eligibility,
    or provides total and attended class counts.

    Args:
        total_classes: Total number of classes conducted.
        attended_classes: Number of classes the student attended.
    """
    if total_classes <= 0:
        return "Error: Total classes must be greater than zero."
    if attended_classes < 0 or attended_classes > total_classes:
        return "Error: Attended classes must be between 0 and total classes."

    percentage = (attended_classes / total_classes) * 100
    eligibility = "✅ Eligible for Exam" if percentage >= 75 else "❌ Not Eligible for Exam"

    return (
        f"📊 Attendance Report\n"
        f"   Total Classes  : {total_classes}\n"
        f"   Classes Attended: {attended_classes}\n"
        f"   Attendance %   : {percentage:.2f}%\n"
        f"   Exam Eligibility: {eligibility}"
    )


# ──────────────────────────────────────────────────────────────
# Tool 2: Result Calculator
# ──────────────────────────────────────────────────────────────
@tool
def result_calculator(
    subject1: float,
    subject2: float,
    subject3: float,
    subject4: float,
    subject5: float,
) -> str:
    """Calculate the average marks, grade, and pass/fail status from marks of 5 subjects.
    Use this tool when the user asks about grades, results, marks, or pass/fail status.

    Args:
        subject1: Marks obtained in subject 1.
        subject2: Marks obtained in subject 2.
        subject3: Marks obtained in subject 3.
        subject4: Marks obtained in subject 4.
        subject5: Marks obtained in subject 5.
    """
    marks = [subject1, subject2, subject3, subject4, subject5]
    average = sum(marks) / len(marks)

    if average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    elif average >= 60:
        grade = "C"
    else:
        grade = "D"

    status = "✅ PASS" if average >= 50 else "❌ FAIL"

    return (
        f"📝 Result Report\n"
        f"   Marks          : {', '.join(str(m) for m in marks)}\n"
        f"   Average Marks  : {average:.2f}\n"
        f"   Grade          : {grade}\n"
        f"   Status         : {status}"
    )


# ──────────────────────────────────────────────────────────────
# Tool 3: Fee Balance Calculator
# ──────────────────────────────────────────────────────────────
@tool
def fee_balance_calculator(total_fee: float, amount_paid: float) -> str:
    """Calculate the pending fee balance for a student.
    Use this tool when the user asks about pending fees, fee balance,
    or remaining course fee amount.

    Args:
        total_fee: Total course fee amount.
        amount_paid: Amount already paid by the student.
    """
    if total_fee < 0 or amount_paid < 0:
        return "Error: Fee amounts cannot be negative."
    if amount_paid > total_fee:
        return f"💰 Overpaid! You have paid ₹{amount_paid - total_fee:.2f} extra."

    pending = total_fee - amount_paid

    return (
        f"💰 Fee Balance Report\n"
        f"   Total Course Fee: ₹{total_fee:.2f}\n"
        f"   Amount Paid     : ₹{amount_paid:.2f}\n"
        f"   Pending Fee     : ₹{pending:.2f}"
    )


# ──────────────────────────────────────────────────────────────
# Tool 4: Library Fine Calculator
# ──────────────────────────────────────────────────────────────
@tool
def library_fine_calculator(delayed_days: int) -> str:
    """Calculate the library fine for late book returns.
    Use this tool when the user asks about library fines, late return charges,
    or overdue book penalties. Fine = ₹5 × Delayed Days.

    Args:
        delayed_days: Number of days the book was returned late.
    """
    if delayed_days < 0:
        return "Error: Delayed days cannot be negative."

    fine = 5 * delayed_days

    return (
        f"📚 Library Fine Report\n"
        f"   Delayed Days: {delayed_days}\n"
        f"   Fine Rate   : ₹5 per day\n"
        f"   Total Fine  : ₹{fine}"
    )


# ──────────────────────────────────────────────────────────────
# Tool 5: Hostel Fee Calculator
# ──────────────────────────────────────────────────────────────
@tool
def hostel_fee_calculator(monthly_fee: float, months_stayed: int) -> str:
    """Calculate the total hostel fee based on monthly rate and duration of stay.
    Use this tool when the user asks about hostel fees or hostel charges.

    Args:
        monthly_fee: Monthly hostel fee amount.
        months_stayed: Number of months the student stayed in the hostel.
    """
    if monthly_fee < 0 or months_stayed < 0:
        return "Error: Values cannot be negative."

    total = monthly_fee * months_stayed

    return (
        f"🏠 Hostel Fee Report\n"
        f"   Monthly Fee  : ₹{monthly_fee:.2f}\n"
        f"   Months Stayed: {months_stayed}\n"
        f"   Total Fee    : ₹{total:.2f}"
    )


# ──────────────────────────────────────────────────────────────
# Bonus Tool: Student Information
# ──────────────────────────────────────────────────────────────
STUDENT_DATABASE = {
    "S001": {
        "name": "Aarav Sharma",
        "branch": "Computer Science",
        "semester": 5,
        "email": "aarav.sharma@college.edu",
        "phone": "9876543210",
        "cgpa": 8.7,
    },
    "S002": {
        "name": "Priya Patel",
        "branch": "Electronics",
        "semester": 3,
        "email": "priya.patel@college.edu",
        "phone": "9876543211",
        "cgpa": 9.2,
    },
    "S003": {
        "name": "Rohan Gupta",
        "branch": "Mechanical",
        "semester": 7,
        "email": "rohan.gupta@college.edu",
        "phone": "9876543212",
        "cgpa": 7.5,
    },
    "S004": {
        "name": "Sneha Reddy",
        "branch": "Civil Engineering",
        "semester": 4,
        "email": "sneha.reddy@college.edu",
        "phone": "9876543213",
        "cgpa": 8.1,
    },
    "S005": {
        "name": "Naman Gupta",
        "branch": "Information Technology",
        "semester": 6,
        "email": "naman.gupta@college.edu",
        "phone": "9876543214",
        "cgpa": 9.0,
    },
}


@tool
def student_info(student_id: str) -> str:
    """Retrieve student details using their Student ID.
    Use this tool when the user asks for student information, student details,
    or provides a student ID (e.g., S001, S002).

    Args:
        student_id: The unique Student ID (e.g., S001, S002, S003).
    """
    student_id = student_id.upper().strip()
    student = STUDENT_DATABASE.get(student_id)

    if not student:
        available = ", ".join(STUDENT_DATABASE.keys())
        return f"❌ Student ID '{student_id}' not found. Available IDs: {available}"

    return (
        f"🎓 Student Information\n"
        f"   Student ID : {student_id}\n"
        f"   Name       : {student['name']}\n"
        f"   Branch     : {student['branch']}\n"
        f"   Semester   : {student['semester']}\n"
        f"   Email      : {student['email']}\n"
        f"   Phone      : {student['phone']}\n"
        f"   CGPA       : {student['cgpa']}"
    )


# ──────────────────────────────────────────────────────────────
# Agent Setup
# ──────────────────────────────────────────────────────────────

# Collect all tools
tools = [
    attendance_calculator,
    result_calculator,
    fee_balance_calculator,
    library_fine_calculator,
    hostel_fee_calculator,
    student_info,
]

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI-powered College Assistant. "
            "You help students with attendance checks, result calculations, "
            "fee balances, library fines, hostel fees, and student information lookups.\n\n"
            "Available tools (use EXACTLY these names):\n"
            "- attendance_calculator: Calculate attendance % and exam eligibility\n"
            "- result_calculator: Calculate average marks, grade, and pass/fail\n"
            "- fee_balance_calculator: Calculate pending fee balance\n"
            "- library_fine_calculator: Calculate library fine for late returns\n"
            "- hostel_fee_calculator: Calculate total hostel fee\n"
            "- student_info: Look up student details by Student ID\n\n"
            "IMPORTANT: When a query contains MULTIPLE requests, you MUST invoke "
            "ALL relevant tools in a single step and then provide a consolidated response. "
            "Do NOT prefix tool names with 'default_api.' — use the exact names above. "
            "Always be helpful, clear, and concise.",
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Initialize LLM via OpenRouter (OpenAI-compatible API)
# To use Ollama instead, replace with:
#   from langchain_ollama import ChatOllama
#   llm = ChatOllama(model="llama3")
import os
import time

api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    api_key = input("Enter your OpenRouter API key: ").strip()

llm = ChatOpenAI(
    model="google/gemini-2.5-flash-lite",  # Cheapest model with tool-calling support
    temperature=0,
    max_tokens=1024,
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
)

# Create the tool-calling agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create the AgentExecutor with verbose=True
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=8,
    handle_tool_error=True,       # Send tool errors back to LLM for retry
    handle_parsing_errors=True,   # Handle malformed LLM outputs gracefully
)

# ──────────────────────────────────────────────────────────────
# Test Cases
# ──────────────────────────────────────────────────────────────


def run_query_with_retry(executor, query, max_retries=3):
    """Run a query with exponential backoff retry on rate-limit errors."""
    for attempt in range(max_retries):
        try:
            result = executor.invoke({"input": query})
            return result
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "rate" in error_msg.lower():
                wait_time = 30 * (attempt + 1)  # 30s, 60s, 90s
                print(f"\n⏳ Rate limited. Waiting {wait_time}s before retry "
                      f"(attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                print(f"\n❌ Error: {e}")
                return {"output": f"Error: {e}"}
    return {"output": "Error: Max retries exceeded due to rate limiting."}


if __name__ == "__main__":
    print("=" * 70)
    print("🎓  AI-Powered College Assistant — LangChain Tool Calling Agent")
    print("=" * 70)

    test_queries = [
        # Query 1 — Attendance
        "I attended 72 classes out of 90. Am I eligible for exams?",
        # Query 2 — Result
        "My marks are 95, 90, 88, 91 and 87. What is my grade?",
        # Query 3 — Fee Balance
        "My course fee is 50000 and I have paid 35000. How much fee is pending?",
        # Query 4 — Library Fine
        "I returned a library book 8 days late. What is the fine amount?",
        # Query 5 — Hostel Fee
        "Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.",
        # Multi-Tool Challenge
        (
            "I attended 80 classes out of 100. "
            "My marks are 90, 85, 88, 92 and 95. "
            "My course fee is 60000 and I paid 45000. "
            "Provide: 1. Attendance Status 2. Grade 3. Pending Fee"
        ),
        # Bonus — Student Info
        "Get me the details of student S002.",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'─' * 70}")
        print(f"📌 Test Case {i}")
        print(f"   Query: {query}")
        print(f"{'─' * 70}")
        result = run_query_with_retry(agent_executor, query)
        print(f"\n🤖 Agent Response:\n{result['output']}")
        print()
        # Delay between queries to avoid rate limiting on free tier
        if i < len(test_queries):
            print("⏳ Waiting 10s before next query (rate-limit courtesy)...")
            time.sleep(10)

