from .class_section import Section
import re

ACTIVE_LOG_FILTERS = [
  # remove timestamps
  # TODO: re-add timestamps (it's here for de-dedupe)
  "^[A-Z][0-9]{4}.{0,25}",

  # end outside window span
  "^.*(node|disk) '.{0,50}' end outside window.*$",

  # success logs
  "^.*ETL: (Asset|Allocation): Save: successfully saved.*$",
  "^.*ETL: (Asset|Allocation)\[1(h|d)\]: run.* completed.*$",
  "^.*ETL: (Asset|Allocation): updated resource totals.*$",
  "^.*ETL: (Asset|Allocation)\[1(h|d)\]: Query.*$",
  "^.*ETL: (Asset|Allocation)\[1(h|d)\]: SummaryQuery.*$",
  "^.*ComputeCostData\: Processing Query Data$",

  # info logs
  "^.*Spot Pricing Refresh scheduled in [0-9]+\.[0-9]+ minutes\.$",
  "^.*Alert Configs Changed. Writing Updated Config to disk.$",
]

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
      search_term = "^\|.*\:kubecost-({})-.*\:(.*)$".format('|'.join(self.POD_REGEXES))
      found = re.search(search_term, section_id)
      self.section_type = found.group(1)
      self.section_id = found.group(2)
    except:
      self.section_type = 'unknown-mini'
      self.section_id = section_id.strip()

  def getLogs(self, bug_report, num_of_lines = False):
    logs = self._getLogs(bug_report, num_of_lines)
    # apply regex filters to clean up logs
    for log_filter in ACTIVE_LOG_FILTERS:
      logs = [re.sub(log_filter, '', i) for i in logs]
    # remove duplicates
    logs = list(set(logs))
    return logs
