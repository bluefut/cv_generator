import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from svglib.svglib import svg2rlg
from reportlab.platypus import PageBreak

# Dynamic title based on candidate name and current date
candidate_name = "Candidate Name"
date_label = datetime.datetime.today().strftime("%B-%Y")
pdf_title = f"{candidate_name} - CV - {date_label}"
file_path = f"{candidate_name} - CV - {date_label}.pdf"
doc = SimpleDocTemplate(file_path, pagesize=A4,
                        rightMargin=30, leftMargin=30,
                        topMargin=30, bottomMargin=30)

styles = getSampleStyleSheet()
dark_blue = colors.HexColor("#303c4f")  # Dark navy
gray_text = colors.HexColor("#676666")

# Styles
style_name = ParagraphStyle(name='Name', parent=styles['Heading1'], alignment=TA_LEFT, 
                            fontSize=24, spaceAfter=8, fontName='Helvetica', textColor=dark_blue)
style_title = ParagraphStyle(name='Title', parent=styles['Normal'], alignment=TA_LEFT, 
                             fontSize=14, textColor=gray_text, spaceAfter=10)
style_summary = ParagraphStyle(name='Summary', parent=styles['Normal'], alignment=TA_LEFT, 
                               fontSize=9, leading=11, textColor=colors.black)
style_contact_right = ParagraphStyle(name='ContactRight', parent=styles['Normal'], alignment=TA_RIGHT, 
                                     fontSize=9, leading=14, textColor=colors.black)
style_sec_header = ParagraphStyle(name='SectionHeader', parent=styles['Heading2'], 
                                  alignment=TA_CENTER, fontSize=12, fontName='Helvetica-Bold', 
                                  textTransform='uppercase', textColor=dark_blue)
style_job_title = ParagraphStyle(name='JobTitle', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold', spaceAfter=1, textColor=colors.black)
style_company = ParagraphStyle(name='Company', parent=styles['Normal'], fontSize=10, fontName='Helvetica', textColor=colors.black, spaceAfter=1)
style_date = ParagraphStyle(name='Date', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Oblique', textColor=gray_text, spaceAfter=4)
style_bullet = ParagraphStyle(name='Bullet', parent=styles['Normal'], fontSize=9, leading=12, alignment=TA_LEFT, spaceAfter=2, leftIndent=0, bulletIndent=0)
style_sub_bullet = ParagraphStyle(name='SubBullet', parent=style_bullet, leftIndent=14)
style_skill_item = ParagraphStyle(name='SkillItem', parent=styles['Normal'], fontSize=9, leading=11, alignment=TA_LEFT)
style_cert_item = ParagraphStyle(name='CertItem', parent=styles['Normal'], fontSize=10, leading=12, alignment=TA_LEFT)
style_tool_label = ParagraphStyle(name='ToolLabel', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Bold', alignment=TA_LEFT)
style_tool_val = ParagraphStyle(name='ToolVal', parent=styles['Normal'], fontSize=9, leading=11, alignment=TA_LEFT)

def add_footer(canvas, doc):
    canvas.saveState()
    # Set PDF metadata title (browser tab title)
    canvas.setTitle(pdf_title)
    canvas.setFont('Helvetica-Oblique', 9)
    canvas.setFillColor(colors.gray)
    page_num_text = "Page %d" % doc.page
    canvas.drawRightString(A4[0] - 40, 20, page_num_text)
    canvas.restoreState()

story = []

# Header content
left_content = []
left_content.append(Paragraph("Candidate Name", style_name))
left_content.append(Paragraph("Product, Security or IT Professional", style_title))
summary_text = (
    "Results-oriented professional with experience supporting and improving digital products, information systems, and cloud environments. Strong skills in troubleshooting, automation, and cross-team communication. Eager to contribute to organizational goals in technology-driven settings."
)
left_content.append(Paragraph(summary_text, style_summary))

def svg_icon(path, width=15, height=15):
    drawing = svg2rlg(path)
    if getattr(drawing, "width", None) and getattr(drawing, "height", None):
        scale_x = width / float(drawing.width)
        scale_y = height / float(drawing.height)
        drawing.width = width
        drawing.height = height
        drawing.scale(scale_x, scale_y)
    return drawing

contact_rows = [
    [Paragraph("<a href='mailto:sample@email.com'>sample@email.com</a>", style_contact_right), svg_icon("mail.svg")],
    [Paragraph("<a href='tel:+10000000000'>+1 000 000 0000</a>", style_contact_right), svg_icon("tel.svg")],
    [Paragraph("City, Country", style_contact_right), svg_icon("location.svg")],
    [Paragraph("<a href='https://linkedin.com/in/sampleuser'>linkedin.com/in/sampleuser</a>", style_contact_right), svg_icon("linkedin.svg")],
]
t_contact = Table(contact_rows, colWidths=[None, 14])
t_contact.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ('LEFTPADDING', (0, 0), (0, -1), 0),
    ('RIGHTPADDING', (0, 0), (0, -1), 6),
    ('LEFTPADDING', (1, 0), (1, -1), 0),
    ('RIGHTPADDING', (1, 0), (1, -1), 0),
    ('TOPPADDING', (0, 0), (-1, -1), 0),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
]))
right_content = [t_contact]
t_header = Table([[left_content, right_content]], colWidths=['60%', '40%'])
t_header.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,-1), 0),
]))
story.append(t_header)
story.append(Spacer(1, 15))

def draw_sandwich_header(text):
    elems = []
    elems.append(HRFlowable(width="100%", thickness=1, color=dark_blue, spaceAfter=0))
    elems.append(Spacer(1, -12))
    elems.append(Paragraph(text, style_sec_header))
    elems.append(Spacer(1, -10))
    elems.append(HRFlowable(width="100%", thickness=1, color=dark_blue, spaceBefore=0))
    elems.append(Spacer(0, 8))
    return elems

# Skills
story.extend(draw_sandwich_header("SKILLS"))
skills_list = [
    "Problem Solving", "System Troubleshooting", "Process Optimization", "End-user Support",
    "Documentation", "Workflow Automation", "Quality Assurance", "Security Awareness",
    "Incident Response", "Remote Collaboration", "Continuous Learning", "Requirements Gathering"
]
rows = []
temp_row = []
for i, skill in enumerate(skills_list):
    temp_row.append(Paragraph(skill, style_skill_item))
    if len(temp_row) == 3:
        rows.append(temp_row)
        temp_row = []
if temp_row:
    while len(temp_row) < 3:
        temp_row.append("")
    rows.append(temp_row)
t_skills = Table(rows, colWidths=['33%', '33%', '33%'])
t_skills.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 20),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 20),
    ('CENTERING', (0,0), (-1,-1), 'CENTERED'),
]))
story.append(t_skills)
story.append(Spacer(1, 10))

# Tools & Technologies
story.extend(draw_sandwich_header("TOOLS & TECHNOLOGIES"))
tools_data = [
    ("Core Tools:", "Security Tool Suite, Productivity Suite, Ticketing Platform"),
    ("Platforms:", "Cloud Platform, Enterprise OS, Virtualization Layer"),
    ("Development/Testing:", "CI/CD, API Tools, Issue Tracker"),
    ("Collaboration Tools:", "Document Sharing, Communication Platform, Analytics Dashboard"),
    ("Concepts/Standards:", "Security Best Practices, API Concepts, Networking Protocols"),
    ("Automation/Scripting:", "Python, Scripting Language, SQL, Markup Language"),
]
tool_rows = []
for label, val in tools_data:
    tool_rows.append([Paragraph(label, style_tool_label), Paragraph(val, style_tool_val)])
t_tools = Table(tool_rows, colWidths=[110, 400])
t_tools.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_tools)
story.append(Spacer(1, 10))

# Experience 
story.extend(draw_sandwich_header("WORK EXPERIENCE"))
def create_job_entry(title, company, date, bullets):
    elems = [
        Paragraph(title, style_job_title),
        Paragraph(company, style_company),
        Paragraph(date, style_date),
    ]
    for b in bullets:
        if isinstance(b, str):
            elems.append(Paragraph(f"• {b}", style_bullet))
        elif isinstance(b, tuple) and len(b) == 2:
            main_text, sub_items = b
            elems.append(Paragraph(f"• {main_text}", style_bullet))
            for sub in sub_items:
                elems.append(Paragraph(f"– {sub}", style_sub_bullet))
    elems.append(Spacer(1, 12))
    return KeepTogether(elems)

b1 = [
    "Provided daily operations and general technical support for digital products.",
    "Coordinated onboarding/training activities to improve knowledge sharing.",
    "Participated in process improvements for customer and end-user workflows.",
    "Supported automation and workflow initiatives using standard tools.",
    (
        "Project/team optimization efforts:",
        [
            "Improved process consistency across teams.",
            "Streamlined incident communication.",
            "Assisted in reducing resolution time for escalations.",
        ],
    ),
]
story.append(create_job_entry("Support Team Lead", "CompanyXYZ", "2021 - 2023", b1))

b2 = [
    "Served as primary contact for end-user incident resolution.",
    "Assisted teams in troubleshooting, configuration, and technical documentation.",
    "Participated in tool integrations and process platform migrations.",
    "Maintained knowledge base and procedural documents.",
]

story.append(create_job_entry("Technical Support Specialist", "CompanyXYZ", "2019 - 2021", b2))

b3 = [
    "Provided general platform and application support.",
    "Guided users in self-service environments.",
    "Identified recurring issues and proposed procedural improvements.",
    "Collaborated across teams to support releases and bug fixes.",
]
story.append(create_job_entry("IT/Application Support", "CompanyXYZ", "2017 - 2019", b3))

b4 = [
    "Assisted teams in feature verification and validation.",
    "Helped create test plans and managed basic research documentation.",
    "Supported cross-team knowledge exchange.",
]
story.append(create_job_entry("QA / Product Support Assistant", "CompanyXYZ", "2016 - 2017", b4))

# Certifications
story.extend(draw_sandwich_header("CERTIFICATIONS"))
certs_list = [
    "Professional Certification A",
    "Professional Certification B",
    "Certificate in Customer Service",
    "Training: Quality Processes"
]
rows = []
temp_row = []
for i, cert in enumerate(certs_list):
    temp_row.append(Paragraph(cert, style_cert_item))
    if len(temp_row) == 2:
        rows.append(temp_row)
        temp_row = []
if temp_row:
    while len(temp_row) < 2: temp_row.append("")
    rows.append(temp_row)
t_certs = Table(rows, colWidths=['50%', '50%'])
t_certs.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ('CENTERING', (0,0), (-1,-1), 'CENTERED'),
]))
story.append(t_certs)
story.append(Spacer(1, 10))

# Education
story.extend(draw_sandwich_header("EDUCATION"))
story.append(Paragraph("<b>Bachelor's Degree in a Technical Field</b>", style_job_title))
story.append(Paragraph("Sample University", style_company))
story.append(Paragraph("2012 - 2017", style_date))
story.append(Spacer(1, 10))

# Languages
story.extend(draw_sandwich_header("LANGUAGES"))
languages = [
    ("English", "Professional Working Proficiency"),
    ("Language B", "Native or Full Proficiency"),
]
lang_cells = []
for lang, level in languages:
    cell_elems = [
        Paragraph(f"<b>{lang}</b>", style_company),
        Paragraph(level, style_date),
    ]
    lang_cells.append(cell_elems)
t_lang = Table([lang_cells], colWidths=['50%', '50%'])
t_lang.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
]))
story.append(t_lang)

if __name__ == "__main__":
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)