from .class_section import Section

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

  def getLogs(self, num_of_lines = False):
    logs = self._getLogs(num_of_lines)
    # apply regex filters to clean up logs
    for log_filter in ACTIVE_LOG_FILTERS:
      logs = [re.sub(log_filter, '', i) for i in logs]
    # remove duplicates
    logs = list(set(logs))
    return logs
