class Section:
  def __init__(self, line_num, seperator):
    self.line_num_start = line_num
    self.line_num_end = 'EOF'
    self.seperator = seperator
  def __str__(self):
    return s.section_type + ' section for ' + s.section_id + ' @ ' + str(s.line_num_start) + '...' + str(s.line_num_end)
  def _getLogs(self, bug_report, num_of_lines = False):
    start_line = self.line_num_start + 2
    end_line = start_line + num_of_lines if num_of_lines else self.line_num_end
    return bug_report[start_line:end_line]
