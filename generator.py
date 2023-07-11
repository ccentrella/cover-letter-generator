from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, pica
from reportlab.lib.pagesizes import letter
import os

# Application specific properties
date = datetime.today().strftime("%m.%d.%y")
type = input("Which format would you like to use? Supported formats are cover letter, "
             "long, medium and short.").lower() or 'cover letter'
company = input("What is the name of the company?\n")

if type == "cover letter":
    hiring_manager = input("What is the recruiter or hiring manager's name?\n").title() or "Hiring Manager"
    role = input("What role are you applying for?\n").title() or "Software Engineer"
    platform = input("Where did you find this position?\n") or "website"

if type in ("cover letter", "medium"):
    line_character = input("If you wish to use a line break character between paragraphs, enter it now.\n") or None

startup_input = input("Is this company a startup?\n").lower() or "no"
startup = "yes" in startup_input or startup_input == "y"

# Parse role shorthand to correct format
match role.lower():
    case 'se':
        role = "Software Engineer"
    case 'seii':
        role = "Software Engineer II"
    case 'seiii':
        role = "Software Engineer III"
    case 'sse':
        role = 'Senior Software Engineer'
    case 'fee':
        role = 'Frontend Engineer'
    case 'bee':
        role = 'Backend Engineer'
    case 'fsse' | 'fse':
        role = "Full Stack Software Engineer"

# Content
# match type:
#     case 'cover letter':
#         content = ''
#     case 'long':
#     case 'medium'
#     case 'short':

# Cover letter content
heading_1 = f"{company} Corporation"
heading_2 = date.__str__()
salutation = f"Dear {hiring_manager},"
introduction = f"I am writing to apply for the {role} role advertised on your {platform}."

if not startup:
    body_1 = f"I've long believed that technology has the power, when united with human insight, to help people, increase efficiency, and create a brighter future. {company}'s passion to create innovative products using cutting edge technology resonates with me, and with my knowledge of fundamental programming and debugging concepts, first hand experience with several technologies, and awareness of software architecture and applications, I have the necessary skills to excel in this position."
else:
    body_1 = "I've long believed that technology has the power, when united with human insight, to help people, increase efficiency, and create a brighter future. I'm really excited to work in a startup environment utilizing cutting-edge technologies to create innovative products that define the future of how we interact with each other. With my knowledge of machine learning and AI, first-hand experience with several frameworks and software architectures, and ability to learn new technologies in a short amount of time, I have the necessary skills to excel in this position."

body_2 = "I have more than 12 months of relevant experience in software and web development, and as a Computer Science Graduate, I gained valuable experience in working on personal apps and web development projects in the last 5 years. Furthermore, I've worked with various AWS technologies including EC2 and Cloud9, and am familiar with their machine learning offerings. My experience so far, combined with my academic and technical knowledge, make me a suitable candidate for the role."
body_3 = "I finished building independently 10+ websites and applications so far, which motivated me to learn further, work harder, and helped me to significantly improve my planning, coding, and problem-solving skills, as well as my work in databases, on different platforms, and in different programming languages."
body_4 = "My most recent successful web project was the HR case study for IBM that included dozens of features."
body_5=f"As these few accomplishments show, I am not only fond of the software development that I do, but I take great pride in it, as well. If given a chance to become a {role} at {company}, I will bring that same work ethic and motivation." 
body_6 = "I also believe that my engagement would make it a much shorter learning curve than usual and that I could achieve even better results at your company."

closing_1 = f"I would welcome the chance to discuss your upcoming projects and plans and show you how my previous achievements can be replicated and improved at {company}."
closing_2 = "Looking forward to speaking with you."
signature_1 = "Sincerely,"
signature_2 = "Christopher Centrella"

# Convert to PDF
title = f'cover_letter_cc_{company.lower()}_{date}.pdf'
doc = SimpleDocTemplate(title, pagesize=letter, bottomMargin = 0.75 * inch)
Story = [Spacer(1,0*inch)]
style = getSampleStyleSheet()['BodyText']
style.fontSize = 11
style.leading = 14
style.spaceAfter = 0.75 * pica

heading_blocks = [heading_1, heading_2]
body_blocks = [salutation, introduction, body_1, body_2, body_3, body_4, body_5, body_6, closing_1, closing_2]
conclusion_blocks = [signature_1, signature_2]

# Add content to file
for block in heading_blocks:
    p = Paragraph(block, style)
    Story.append(p)
Story.append(Spacer(1, 1*pica))

style.spaceAfter = 1.25 * pica
for block in body_blocks:
    p = Paragraph(block, style)
    Story.append(p)
    if line_character != None:
        Story.append(Paragraph(line_character))
Story.append(Spacer(1, 1*pica))

style.spaceAfter = 0.75 * pica
for block in conclusion_blocks:
    p = Paragraph(block, style)
    Story.append(p)

doc.build(Story)

path = os.path.join(os.getcwd(), title)
print(f"Created successfully: {path}\n")
print(f"Details: role = {role}, company = {company}, platform = {platform}, startup = {startup}, hiring manager = {hiring_manager}\n")