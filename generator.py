from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, pica
from reportlab.lib.pagesizes import letter
import os
import json

class Generator:

    @classmethod
    def __init__(cls):
        cls.date = datetime.today()
        cls.graph_data = {}
        cls.heading_blocks = []
        cls.body_blocks = []
        cls.conclusion_blocks = []
        cls.line_character = None
        cls.title = None

    @classmethod
    def create_document(cls):
        type = input("Which format would you like to use? Supported formats are cover letter, "
             "long, medium and short. Default is cover letter.\n").lower()
        match type:
            case 'long' | 'long summary' | 'summary long':
                cls.prepare_long_summary()
            case 'medium' | 'medium summary' | 'summary medium':
                cls.prepare_medium_summary()
            case 'short' | 'short summary' | 'summary short':
                cls.prepare_short_summary()
            case default:
                cls.prepare_cover_letter()

        cls.line_character = input("If you wish to use a line break character between paragraphs, enter it now.\n") or ''

        use_file_input = input("Would you like to generate a file?\n").lower() or "no"
        if "yes" in use_file_input or use_file_input == "y":
            cls.write_pdf()
        else:
            cls.write_terminal()

    # Prepare using specified format        
    @classmethod
    def prepare_cover_letter(cls):
        company = None
        while not company:
            company = input("What is the name of the company?\n")
        hiring_manager = input("What is the recruiter or hiring manager's name?\n").title() or "Hiring Manager"

        role_input = input("What role are you applying for?\n").title()
        role = Generator.parse_role(role_input)
        platform = input("Where did you find this position?\n") or None

        cls.load_file('formats/cover-letter.json')

        heading_1 = f'{company} {cls.graph_data["heading"]}'
        heading_2 = cls.date.strftime("%m.%d.%y")

        salutation = f'{cls.graph_data["salutation"]} {hiring_manager},'

        if platform is None:
            body_1 = f'{cls.graph_data["body"]["line1"]["part1"]} {role} {cls.graph_data["body"]["line1"]["part2"]} {company}.'
        else:
            body_1 = f'{cls.graph_data["body"]["line1"]["part1"]} {role} {cls.graph_data["body"]["line1"]["part2"]} {company},'
            f'which I found on {platform}.'
        body_2 = f'{cls.graph_data["body"]["line2"]["part1"]} {role}, {cls.graph_data["body"]["line2"]["part2"]}'
        body_3 = f'{cls.graph_data["body"]["line3"]}'
        body_4 = f'{cls.graph_data["body"]["line4"]}'
        body_5 = f'{cls.graph_data["body"]["line5"]}'
        body_6 = f'{cls.graph_data["body"]["line6"]["part1"]} {company} {cls.graph_data["body"]["line6"]["part2"]}'

        complimentary_close_1 = f'{cls.graph_data["complimentaryClose"]["line1"]}'
        complimentary_close_2 = f'{cls.graph_data["complimentaryClose"]["line2"]}'

        signature = f'{cls.graph_data["signature"]}'

        cls.heading_blocks = [heading_1, heading_2]
        cls.body_blocks = [salutation, body_1, body_2, body_3, body_4, body_5, body_6, complimentary_close_1, complimentary_close_2]
        cls.conclusion_blocks = [signature]
        cls.title = f'cover_letter_cc_{company.lower()}_{cls.date.strftime("%m.%d.%y")}.pdf'
    
    @classmethod
    def prepare_long_summary(cls):
        role_input = input("What role are you applying for?\n").title()
        role = Generator.parse_role(role_input)

        cls.load_file('formats/summary-long.json')
        body_1 = f'{cls.graph_data["body"]["line1"]["part1"]} {role}, {cls.graph_data["body"]["line1"]["part2"]}'
        body_2 = f'{cls.graph_data["body"]["line2"]}'
        body_3 = f'{cls.graph_data["body"]["line3"]}'
        body_4 = f'{cls.graph_data["body"]["line4"]}'

        cls.body_blocks = [body_1, body_2, body_3, body_4]
        cls.title = f'summary_long_cc_{cls.date.isoformat()}.pdf'
    
    @classmethod
    def prepare_medium_summary(cls):
        cls.load_file('formats/summary-medium.json')
        content = f'{cls.graph_data["body"]["line1"]}'
        
        cls.body_blocks = [content]   
        cls.title = f'summary_medium_cc_{cls.date.isoformat()}.pdf'
    
    @classmethod
    def prepare_short_summary(cls):
        cls.load_file('formats/summary-short.json')
        content = f'{cls.graph_data["body"]["line1"]}'
        
        cls.body_blocks = [content]
        cls.title = f'summary_short_cc_{cls.date.isoformat()}.pdf'

    @staticmethod
    def parse_role(role):
        if not role:
            return "Software Engineer"
        
        match role.lower():
            case 'se':
                return "Software Engineer"
            case 'seii':
                return "Software Engineer II"
            case 'seiii':
                return "Software Engineer III"
            case 'sse':
                return 'Senior Software Engineer'
            case 'fee':
                return 'Frontend Engineer'
            case 'bee':
                return 'Backend Engineer'
            case 'fsse' | 'fse':
                return "Full Stack Software Engineer"
            case default:
                return role
    
    @classmethod
    def load_file(cls, file_location):
        with open(file_location, 'r') as file:
            data = file.read()
            cls.graph_data = json.loads(data)
   
    # Output document
    @classmethod
    def write_pdf(cls):

        # Initialize PDF document
        doc = SimpleDocTemplate(cls.title, pagesize=letter, bottomMargin = 0.75 * inch)
        Story = [Spacer(1,0*inch)]
        style = getSampleStyleSheet()['BodyText']
        style.fontSize = 11
        style.leading = 14
        style.spaceAfter = 0.75 * pica

        # Add content to file
        for block in cls.heading_blocks:
            p = Paragraph(block, style)
            Story.append(p)
        Story.append(Spacer(1, 1*pica))

        style.spaceAfter = 1.25 * pica
        for block in cls.body_blocks:
            p = Paragraph(block, style)
            Story.append(p)
            Story.append(Paragraph(cls.line_character))
        Story.append(Spacer(1, 1*pica))

        style.spaceAfter = 0.75 * pica
        for block in cls.conclusion_blocks:
            p = Paragraph(block, style)
            Story.append(p)

        doc.build(Story)

        path = os.path.join(os.getcwd(), cls.title)
        print(f"Created successfully: {path}\n")
    
    @classmethod
    def write_terminal(cls):
        for block in cls.heading_blocks:
            print(block)
            print(cls.line_character)
        if len(cls.heading_blocks) > 0:
            print()

        for block in cls.body_blocks:
            print(block)
            print(cls.line_character)
        print()

        for block in cls.conclusion_blocks:
            print(block)
            print(cls.line_character)
        if len(cls.conclusion_blocks) > 0:
            print()

# Start Generator
generator = Generator()
generator.create_document()
