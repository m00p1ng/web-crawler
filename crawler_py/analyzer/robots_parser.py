import re
from ..utils import print_log
from ..database import db


class RobotsParser:
    def __init__(self, hostname, content):
        self.hostname = hostname
        self.content = content

    def extract_link(self):
        print_log("Extracting robots.txt")
        lines = self._split_lines()
        for i, line in enumerate(lines):
            if re.match(r'^User-agent: \*', line):
                self._match_disallow_link(i + 1, lines)
                break

    def _split_lines(self):
        lines = self.content.split('\n')
        lines = [line.strip() for line in lines]
        return lines

    def _match_disallow_link(self, i, lines):
        print_log(f"Adding '{self.hostname}' disallow lists")
        while i < len(lines) and not re.match(r'^User-agent', lines[i]):
            result = re.match(r'^Disallow: (.*)', lines[i])
            if result:
                self._save_disallow_link(result.group(1))
            i += 1
        print_log(f"'{self.hostname}' disallow lists were added\n")

    def _save_disallow_link(self, resource):
        COLLECTION = 'disallow_link'

        data = {
            "hostname": self.hostname,
            "resource": resource,
        }
        if not db[COLLECTION].find_one(data):
            db[COLLECTION].insert(data)
