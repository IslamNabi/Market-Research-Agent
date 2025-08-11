from config import GOOGLE_API_KEY, GOOGLE_CSE_ID

from modules.planner import Planner
from modules.researcher import Researcher
from modules.summarizer import Summarizer
from modules.analyzer import Analyzer
from modules.pdf_generator import PDFGenerator
from modules.email_sender import EmailSender

def main():
    goal = "Find top 10 AI startups in Pakistan and create a market research report."

    # Step 1: Plan
    planner = Planner()
    steps = planner.create_plan(goal)
    print("Plan:", steps)

    # Step 2: Research (Google Custom Search)
    researcher = Researcher(api_key=GOOGLE_API_KEY, cse_id=GOOGLE_CSE_ID)
    data = researcher.search("Top AI startups in Pakistan", num_results=10)

    # Step 3: Summarize
    summarizer = Summarizer()
    summary = summarizer.summarize_market(data)

    # Step 4: Analyze
    analyzer = Analyzer()
    df = analyzer.to_dataframe(data)
    stats, charts, *_ = analyzer.basic_stats_and_charts(df, slug="report")

    print("Stats:", stats)
    print("Charts generated:", charts)

    # Step 5: Generate PDF (with charts embedded)
    pdf_gen = PDFGenerator()
    pdf_path = pdf_gen.create_report(summary, "market_research_report", charts=charts, stats=stats)

    # Step 6: Send Email
    email_sender = EmailSender()
    email_sender.send_email(
        recipient="recipient@example.com",
        subject="Market Research Report",
        body="Please find attached the market research report.",
        attachment_path=pdf_path
    )

    print("✅ Report generated and sent!")

if __name__ == "__main__":
    main()
