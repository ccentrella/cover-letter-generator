from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, pica
from reportlab.lib.pagesizes import letter
import shutil
import os
import pathlib
import json

class Generator:

    def __init__(self):
        self.date = datetime.today()
        self.graph_data = {}
        self.env = {}
        self.heading_blocks = []
        self.body_blocks = []
        self.conclusion_blocks = []
        self.line_character = None
        self.title = None

        self.load_environment_variables()

    def load_environment_variables(self):
        with open(".env", 'r', encoding="utf-8") as file:
            dictionary = {}
            for line in file.readlines():
                comment_index = line.find('#')
                equals_index = line.find('=')

                if comment_index == -1:
                    comment_index = len(line)
                if equals_index > 0 and equals_index + 1 < comment_index:
                    key = line[:equals_index].upper()
                    value = line[equals_index + 1 : comment_index].replace('\n','')
                    dictionary[key] = value

            self.env = dictionary

    def create_document(self):
        create_pdf = False
        type = input("Which format would you like to use? Supported formats are cover letter, "
             "long summary, medium summary and short summary. Default is long summary.\n").lower()
        match type:
            case 'c' | 'cl'| 'l' | 'cover' | 'cover letter' | 'letter':
                self.prepare_cover_letter()
                create_pdf = True
            case 's' | 'ss' | 'short' | 'short summary' | 'summary short':
                self.prepare_short_summary()
            case 'm' | 'ms' | 'sm' | 'medium' | 'medium summary' | 'summary medium':
                self.prepare_medium_summary()
            case default:
                self.prepare_long_summary()

        self.line_character = input("Optional: If you wish to use a line break character between paragraphs, enter it now.\n") or ''

        if create_pdf:
            create_pdf_text = "Optional: Enter no to prevent generating a pdf.\n"
        else:
            create_pdf_text = "Optional: Enter yes to generate a pdf.\n"
        create_pdf_input = input(create_pdf_text).lower()
        if "yes" in create_pdf_input or create_pdf_input == "y":
            create_pdf = True
        elif "no" in create_pdf_input or create_pdf_input == "n":
            create_pdf = False

        os.system('clear')
        self.write_terminal()

        if create_pdf:
            self.write_pdf()

    # Prepare using specified format
    def prepare_cover_letter(self):
        company = None
        while not company:
            company = input("What is the name of the company?\n")
        hiring_manager = input("Optional: What is the recruiter or hiring manager's name?\n").title() or "Hiring Manager"

        role_input = input("Optional: What role are you applying for?\n").title()
        role = Generator.parse_role(role_input)
        platform = input("Optional: Where did you find this position?\n") or None

        self.load_format('formats/cover-letter.json')

        heading_1 = f'{company} {self.graph_data["heading"]}'
        heading_2 = self.date.strftime("%m.%d.%y")

        salutation = f'{self.graph_data["salutation"]} {hiring_manager},'

        if platform is None:
            body_1 = f'{self.graph_data["body"]["line1"]["part1"]} {role} {self.graph_data["body"]["line1"]["part2"]} {company}.'
        else:
            body_1 = f'{self.graph_data["body"]["line1"]["part1"]} {role} {self.graph_data["body"]["line1"]["part2"]} {company},'
            f'which I found on {platform}.'
        body_2 = f'{self.graph_data["body"]["line2"]["part1"]} {role}, {self.graph_data["body"]["line2"]["part2"]}'
        body_3 = f'{self.graph_data["body"]["line3"]}'
        body_4 = f'{self.graph_data["body"]["line4"]}'
        body_5 = f'{self.graph_data["body"]["line5"]["part1"]} {company} {self.graph_data["body"]["line5"]["part2"]}'

        complimentary_close = f'{self.graph_data["complimentaryClose"]["part1"]} {self.env["EMAIL"]} ' \
        f'{self.graph_data["complimentaryClose"]["part2"]} {self.env["PHONE"]}. {self.graph_data["complimentaryClose"]["part3"]}'

        signature = f'{self.graph_data["signature"]}'

        self.heading_blocks = [heading_1, heading_2]
        self.body_blocks = [salutation, body_1, body_2, body_3, body_4, body_5, complimentary_close]
        self.conclusion_blocks = [signature]
        self.title = f'cover_letter_cc_{company.lower()}_{self.date.strftime("%m.%d.%y")}.pdf'

    def prepare_long_summary(self):
        role_input = input("Optional: What role are you applying for?\n").title()
        role = Generator.parse_role(role_input)

        self.load_format('formats/summary-long.json')
        body_1 = f'{self.graph_data["body"]["line1"]["part1"]} {role}, {self.graph_data["body"]["line1"]["part2"]}'
        body_2 = f'{self.graph_data["body"]["line2"]}'
        body_3 = f'{self.graph_data["body"]["line3"]}'

        self.body_blocks = [body_1, body_2, body_3]
        self.title = f'summary_long_cc_{self.date.isoformat()}.pdf'

    def prepare_medium_summary(self):
        self.load_format('formats/summary-medium.json')
        content = f'{self.graph_data["body"]["line1"]}'
        
        self.body_blocks = [content]   
        self.title = f'summary_medium_cc_{self.date.isoformat()}.pdf'

    def prepare_short_summary(self):
        self.load_format('formats/summary-short.json')
        content = f'{self.graph_data["body"]["line1"]}'
        
        self.body_blocks = [content]
        self.title = f'summary_short_cc_{self.date.isoformat()}.pdf'

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

    def load_format(self, file_location):
        with open(file_location, 'r', encoding="utf-8") as file:
            data = file.read()
            self.graph_data = json.loads(data)
    
    # Output document
    def write_pdf(self):
        Generator.print_line()
        print('Creating pdf...')

        # Initialize pdf document
        pathlib.Path("applications").mkdir(exist_ok=True)
        location = os.path.join('applications', self.title)
        doc = SimpleDocTemplate(location, pagesize=letter, bottomMargin = 0.75 * inch)
        Story = [Spacer(1,0*inch)]
        style = getSampleStyleSheet()['BodyText']
        style.fontSize = 11
        style.leading = 14
        style.spaceAfter = 0.75 * pica

        # Add content to file
        for block in self.heading_blocks:
            p = Paragraph(block, style)
            Story.append(p)
        Story.append(Spacer(1, 1*pica))

        style.spaceAfter = 1.25 * pica
        for block in self.body_blocks:
            p = Paragraph(block, style)
            Story.append(p)
            Story.append(Paragraph(self.line_character))
        Story.append(Spacer(1, 1*pica))

        style.spaceAfter = 0.75 * pica
        for block in self.conclusion_blocks:
            p = Paragraph(block, style)
            Story.append(p)

        doc.build(Story)

        path = os.path.join(os.getcwd(), 'applications', self.title)
        print(f"Created pdf successfully: {path}\n")

    def write_terminal(self):
        print("Outputting to terminal...\n")
        Generator.print_line()
        os.system('clear')
        print()

        for block in self.heading_blocks:
            print(block)
            print(self.line_character)
        if len(self.heading_blocks) > 0:
            print()

        for block in self.body_blocks:
            print(block)
            print(self.line_character)
        print()

        for block in self.conclusion_blocks:
            print(block)
            print(self.line_character)
        if len(self.conclusion_blocks) > 0:
            print()

    @staticmethod
    def print_line():
        terminal_length, _ = shutil.get_terminal_size((40, 20))
        for _ in range(terminal_length):
            print('-', end='')
        print('\n')

# Start Generator
generator = Generator()
generator.create_document()
