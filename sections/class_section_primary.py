from .class_section import Section

class PrimarySection(Section):
  SEPERATOR = '=' * 128 + '\n'
  def __init__(self, line_num, section_id):
    Section.__init__(self, line_num, self.SEPERATOR)
    self.section_id = section_id.strip()
    self.section_type = 'primary'
