from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import re

class PDFGenerator:
    def __init__(self, filename=None):
        """
        Initialize PDFGenerator with enhanced styling options.
        """
        # Default save directory inside 'data/reports'
        self.save_dir = os.path.join("data", "reports")
        os.makedirs(self.save_dir, exist_ok=True)

        if filename:
            self.filename = filename
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.filename = os.path.join(self.save_dir, f"report_{timestamp}.pdf")

        self.styles = getSampleStyleSheet()

        # Custom color palette
        self.primary_color = "#2C3E50"  # Dark blue
        self.secondary_color = "#3498DB"  # Bright blue
        self.accent_color = "#E74C3C"  # Red
        self.light_gray = "#F5F5F5"
        self.dark_gray = "#333333"

        # Enhanced styles
        self.styles.add(ParagraphStyle(
            name='TitleModern',
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=24,
            textColor=self.primary_color,
            fontName='Helvetica-Bold',
            underline=True,
            underlineColor=self.secondary_color,
            underlineWidth=1
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            fontSize=16,
            leading=22,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=8,
            textColor=self.primary_color,
            fontName='Helvetica-Bold',
            leftIndent=0,
            borderLeft=4,
            borderColor=self.secondary_color,
            borderPadding=(0, 0, 0, 10)
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyModern',
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            textColor=self.dark_gray,
            fontName='Helvetica'
        ))
        
        self.styles.add(ParagraphStyle(
            name='BulletModern',
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            textColor=self.dark_gray,
            fontName='Helvetica',
            leftIndent=10,
            bulletIndent=0,
            bulletFontName='Helvetica-Bold',
            bulletFontSize=11
        ))

    def _clean_text(self, text):
        """
        Remove hash symbols (#) and stars (*) from the text.
        """
        # Remove hash symbols
        text = re.sub(r'#+\s*', '', text)
        # Remove stars but keep the text
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove **bold** markers
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Remove *italic* markers
        text = re.sub(r'\*\s?', '', text)               # Remove standalone * used as bullets
        return text.strip()

    def _split_summary_into_sections(self, summary):
        """
        Splits summary text into sections based on natural headings.
        """
        sections = []
        cleaned_summary = self._clean_text(summary)
        
        # Split by potential headings (lines that end with colon or are in all caps)
        pattern = r"(?:\n|^)([A-Z][A-Za-z ]+[:\-]?)\n"
        parts = re.split(pattern, cleaned_summary)
        
        # The first part is usually content before any heading
        if parts[0].strip():
            sections.append(("Introduction", parts[0].strip()))
        
        # Process remaining parts in pairs (heading, content)
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                heading = parts[i].strip().rstrip(':').strip()
                content = parts[i + 1].strip()
                if heading and content:
                    sections.append((heading, content))
        
        # If no headings found, split by double newlines
        if len(sections) == 0:
            paragraphs = [p.strip() for p in cleaned_summary.split("\n\n") if p.strip()]
            for para in paragraphs:
                # Try to extract heading from first sentence
                first_line = para.split('\n')[0]
                if len(first_line.split()) < 8 and first_line.endswith(':'):
                    heading = first_line[:-1]
                    content = '\n'.join(para.split('\n')[1:]).strip()
                    sections.append((heading, content))
                else:
                    sections.append(("Key Information", para))
        
        return sections

    def _add_header_footer(self, canvas, doc):
        """
        Add header and footer to each page.
        """
        canvas.saveState()
        # Header
        canvas.setFont('Helvetica', 10)
        canvas.setFillColor(colors.HexColor(self.primary_color))
        canvas.drawString(inch, doc.pagesize[1] - 0.5 * inch, "Market Research Report")
        canvas.line(inch, doc.pagesize[1] - 0.6 * inch, doc.pagesize[0] - inch, doc.pagesize[1] - 0.6 * inch)
        
        # Footer
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor(self.dark_gray))
        page_num = f"Page {canvas.getPageNumber()}"
        canvas.drawCentredString(doc.pagesize[0]/2, 0.5 * inch, page_num)
        canvas.line(inch, 0.7 * inch, doc.pagesize[0] - inch, 0.7 * inch)
        canvas.restoreState()

    def _format_bullet_points(self, text):
        """
        Format bullet points in the text.
        """
        # Replace numbered lists with proper bullet points
        text = re.sub(r"(\d+\.)\s", "• ", text)
        return text

    def create_report(self, summary, filename=None, stats=None):
        """
        Create PDF report with clean headings and professional formatting.
        """
        if filename:
            self.filename = os.path.join(self.save_dir, os.path.basename(filename))
        if not self.filename:
            raise ValueError("No filename provided for PDF report.")

        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        doc = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            leftMargin=1.5*cm,
            rightMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        doc.build = lambda elements: SimpleDocTemplate.build(
            doc, 
            elements, 
            onFirstPage=self._add_header_footer,
            onLaterPages=self._add_header_footer
        )

        elements = []

        # Title
        elements.append(Paragraph("Market Research Report", self.styles['TitleModern']))
        elements.append(Spacer(1, 24))

        # Date
        today_str = datetime.today().strftime('%B %d, %Y')
        date_style = ParagraphStyle(
            'DateStyle',
            parent=self.styles['BodyModern'],
            alignment=TA_CENTER,
            textColor=self.secondary_color,
            fontSize=11,
            spaceAfter=24
        )
        elements.append(Paragraph(f"Report Generated: {today_str}", date_style))
        elements.append(Spacer(1, 12))

        # Summary as Sections
        sections = self._split_summary_into_sections(summary)
        for heading, content in sections:
            # Format bullet points
            content = self._format_bullet_points(content)
            
            # Add heading (make sure it's title case)
            heading = heading.title()
            elements.append(Paragraph(heading, self.styles['SectionHeader']))
            
            # Split content into paragraphs
            paragraphs = [p.strip() for p in content.split("\n") if p.strip()]
            for para in paragraphs:
                if para.startswith("•"):
                    elements.append(Paragraph(para, self.styles['BulletModern']))
                else:
                    elements.append(Paragraph(para, self.styles['BodyModern']))
            
            elements.append(Spacer(1, 12))

        # Optional Statistics
        if stats:
            elements.append(Paragraph("Key Statistics", self.styles['SectionHeader']))
            
            stat_data = [["Metric", "Value"]]
            for key, value in stats.items():
                stat_data.append([key, str(value)])
            
            stat_table = Table(stat_data, colWidths=[doc.width/2.5, doc.width/2.5])
            stat_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.primary_color)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(self.light_gray)),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.secondary_color)),
            ]))
            
            elements.append(stat_table)
            elements.append(Spacer(1, 24))

        doc.build(elements)
        return self.filename