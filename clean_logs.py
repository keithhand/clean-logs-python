#!/usr/bin/env python3
import argparse, re, linecache

p_description = 'Clean kubecost-bug-report files.'
parser = argparse.ArgumentParser(description=p_description)
parser.add_argument('bug_report_file', type=str, help='.txt file generated by Kubecost')
args = parser.parse_args()

ACTIVE_LOG_FILTERS = [
  # remove timestamps
  "^.{0,30}",

  # end outside window spam
  "^.*(node|disk) '.{0,50}' end outside window.*$",

  # success logs
  "^.*ETL\: (Asset|Allocation)\: Save\: successfully saved.*$",
  "^.*ETL\: (Asset|Allocation)\[1(h|d)\]\: run.* completed.*$",
  "^.*ETL\: (Asset|Allocation)\: updated resource totals.*$",
  "^.*ETL\: (Asset|Allocation)\[1(h|d)\]\: Query.*$",
  "^.*ComputeCostData\: Processing Query Data$",
]


bug_report = None
class Section:
  def __init__(self, line_num, seperator):
    self.line_num_start = line_num
    self.line_num_end = 'EOF'
    self.seperator = seperator
  def __str__(self):
    return s.section_type + ' section for ' + s.section_id + ' @ ' + str(s.line_num_start) + '...' + str(s.line_num_end)
  def getLogs(self, num_of_lines = False):
    start_line = self.line_num_start + 2
    end_line = start_line + num_of_lines if num_of_lines else self.line_num_end
    return bug_report[start_line:end_line]


class PrimarySection(Section):
  SEPERATOR = '=' * 128 + '\n'
  def __init__(self, line_num, section_id):
    Section.__init__(self, line_num, self.SEPERATOR)
    self.section_id = section_id.strip()
    self.section_type = 'primary'


class MiniSection(Section):
  POD_REGEXES = [
    'cost-analyzer',
    'prometheus-server',
    'thanos-query',
    'thanos-sidecar',
    'thanos-compact',
    'thanos-store',
  ]
  SEPERATOR = '+' + '-' * 85 + '\n'
  def __init__(self, line_num, section_id):
    Section.__init__(self, line_num, self.SEPERATOR)
    self.formatSectionId(section_id)

  def formatSectionId(self, section_id):
    try:
      search_term = "^\| \*\*\:kubecost-v2-({})-.*\:(.*)$".format('|'.join(self.POD_REGEXES))
      found = re.search(search_term, section_id)
      self.section_type = found.group(1)
      self.section_id = found.group(2)
    except:
      self.section_type = 'unknown-mini'
      self.section_id = section_id.strip()


primary_sections=[]
mini_sections=[]
with open(args.bug_report_file) as bug_report_file:
  bug_report = bug_report_file.readlines()
  # find all sections seperations
  for num, line in enumerate(bug_report, 1):
    if PrimarySection.SEPERATOR in line:
      if bug_report[num + 1] == PrimarySection.SEPERATOR:
        new_section = PrimarySection(num, bug_report[num])
        if len(primary_sections) > 0:
          primary_sections[-1].line_num_end = new_section.line_num_start - 1
        primary_sections.append(new_section)
    if MiniSection.SEPERATOR in line:
      if bug_report[num + 1] == MiniSection.SEPERATOR:
        new_section = MiniSection(num, bug_report[num])
        if len(mini_sections) > 0:
          mini_sections[-1].line_num_end = new_section.line_num_start - 1
        mini_sections.append(new_section)

def cleanCostModelLogs(cost_model_section):
  print(cost_model_section.getLogs(10))

# find last line in each section
for i, s in enumerate(mini_sections):
  if s.section_id == 'cost-model':
    cleanCostModelLogs(s)
