import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

class PDFGenerator:
    def __init__(self, output_dir="data/reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def create_report(self, summary, filename, charts=None, stats=None):
        """
        Creates a PDF report with summary, optional statistics, and charts.

        :param summary: Text summary of the market research.
        :param filename: Name of the output file without extension.
        :param charts: List of file paths to chart images.
        :param stats: Dictionary containing statistical information.
        :return: Path to generated PDF file.
        """
        pdf_path = os.path.join(self.output_dir, f"{filename}.pdf")
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Add title
        story.append(Paragraph("<b>Market Research Report</b>", styles["Title"]))
        story.append(Spacer(1, 12))

        # Add summary
        story.append(Paragraph("<b>Summary:</b>", styles["Heading2"]))
        story.append(Paragraph(summary, styles["Normal"]))
        story.append(Spacer(1, 12))

        # Add statistics if available
        if stats and isinstance(stats, dict):
            story.append(Paragraph("<b>Statistics:</b>", styles["Heading2"]))
            for key, value in stats.items():
                story.append(Paragraph(f"{key}: {value}", styles["Normal"]))
            story.append(Spacer(1, 12))

        # Add charts if available
        if charts and isinstance(charts, list):
            story.append(Paragraph("<b>Charts:</b>", styles["Heading2"]))
            for chart_path in charts:
                if os.path.exists(chart_path):
                    story.append(Image(chart_path, width=400, height=300))
                    story.append(Spacer(1, 12))
                else:
                    story.append(Paragraph(f"Chart not found: {chart_path}", styles["Normal"]))

        doc.build(story)
        return pdf_path
