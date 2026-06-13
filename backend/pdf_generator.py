from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from datetime import datetime
import io

def generate_pdf_report(filename, total_logs, summary, errors, ai_analysis):
    buffer = io.BytesIO()
    report_name = filename.replace('.log', '').replace('.txt', '')
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=60, leftMargin=60,
                            topMargin=60, bottomMargin=60,
                            title=f"{report_name} - AI Log Report",
                            author="AI Log Intelligence Assistant")

    elements = []

    # Color palette
    purple = HexColor('#6366f1')
    dark = HexColor('#1a202c')
    gray = HexColor('#718096')
    light_gray = HexColor('#f7fafc')
    red = HexColor('#e53e3e')
    orange = HexColor('#dd6b20')
    blue = HexColor('#3182ce')
    pink = HexColor('#d53f8c')
    white = colors.white

    # Styles
    def style(name, size, bold=False, color=dark, space_after=6, indent=0, leading=None):
        return ParagraphStyle(name,
            fontSize=size,
            fontName='Helvetica-Bold' if bold else 'Helvetica',
            textColor=color,
            spaceAfter=space_after,
            leftIndent=indent,
            leading=leading or size * 1.4)

    # ─── HEADER ───
    elements.append(Paragraph("AI Log Intelligence Report", style('title', 26, bold=True, color=purple, space_after=4)))
    elements.append(Paragraph("Automated Log Analysis & Root Cause Detection", style('sub', 12, color=gray, space_after=4)))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", style('date', 10, color=gray, space_after=2)))
    elements.append(Paragraph(f"File: {filename}", style('file', 10, color=gray, space_after=16)))
    elements.append(HRFlowable(width="100%", thickness=2, color=purple, spaceAfter=20))

    # ─── OVERVIEW ───
    elements.append(Paragraph("Overview", style('h2', 14, bold=True, color=dark, space_after=10)))

    overview_data = [
        ['Total Logs Analyzed', 'Errors Found', 'Warnings', 'Critical Events'],
        [
            str(total_logs),
            str(summary.get('ERROR', 0)),
            str(summary.get('WARNING', 0)),
            str(summary.get('CRITICAL', 0))
        ]
    ]

    overview_table = Table(overview_data, colWidths=[130, 130, 130, 130])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), purple),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BACKGROUND', (0,1), (-1,1), light_gray),
        ('TEXTCOLOR', (0,1), (-1,1), dark),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (-1,1), 14),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e2e8f0')),
    ]))
    elements.append(overview_table)
    elements.append(Spacer(1, 24))

    # ─── LOG BREAKDOWN ───
    elements.append(Paragraph("Log Level Breakdown", style('h2', 14, bold=True, color=dark, space_after=10)))

    level_colors = {'INFO': blue, 'WARNING': orange, 'ERROR': red, 'CRITICAL': pink}
    breakdown_data = [['Log Level', 'Count', 'Percentage']]
    for level, count in summary.items():
        pct = f"{round(count / (total_logs or 1) * 100, 1)}%"
        breakdown_data.append([level, str(count), pct])

    breakdown_table = Table(breakdown_data, colWidths=[200, 100, 100])
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), purple),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, light_gray]),
        ('TEXTCOLOR', (0,1), (-1,-1), dark),
    ]
    for i, (level, _) in enumerate(summary.items(), start=1):
        color = level_colors.get(level, dark)
        style_cmds.append(('TEXTCOLOR', (0,i), (0,i), color))
        style_cmds.append(('FONTNAME', (0,i), (0,i), 'Helvetica-Bold'))

    breakdown_table.setStyle(TableStyle(style_cmds))
    elements.append(breakdown_table)
    elements.append(Spacer(1, 24))

    # ─── ERRORS ───
    elements.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#e2e8f0'), spaceAfter=16))
    elements.append(Paragraph("Detected Errors & Critical Events", style('h2', 14, bold=True, color=dark, space_after=10)))

    for i, e in enumerate(errors, 1):
        level_color = pink if e.get('level') == 'CRITICAL' else red
        elements.append(Paragraph(
            f"<b>{i}. [{e.get('date','') } {e.get('time','')}]</b> "
            f"<font color='#{level_color.hexval()[2:]}'>{e.get('level','')}</font>: {e.get('message','')}",
            style(f'err{i}', 10, color=dark, space_after=8, indent=10, leading=16)
        ))

    elements.append(Spacer(1, 20))

    # ─── AI ANALYSIS ───
    elements.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#e2e8f0'), spaceAfter=16))
    elements.append(Paragraph("AI Root Cause Analysis", style('h2', 14, bold=True, color=dark, space_after=10)))

    # Add purple left border box
    ai_data = [[Paragraph(ai_analysis.replace('\n', '<br/>'),
                          style('ai', 11, color=dark, space_after=0, leading=18))]]
    ai_table = Table(ai_data, colWidths=[460])
    ai_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_gray),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LINEBEFORE', (0,0), (0,-1), 4, purple),
        ('GRID', (0,0), (-1,-1), 0, white),
    ]))
    elements.append(ai_table)
    elements.append(Spacer(1, 24))

    # ─── FOOTER ───
    elements.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#e2e8f0'), spaceAfter=8))
    elements.append(Paragraph(
        "Generated by AI Log Intelligence Assistant | HCLtech Internship Project",
        style('footer', 9, color=gray, space_after=0)
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer