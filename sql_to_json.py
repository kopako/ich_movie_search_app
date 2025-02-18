import re
from datetime import datetime

class SQLToJSON:
    select_pattern = re.compile(r'SELECT\s+(.+?)\s+FROM', re.IGNORECASE | re.DOTALL)
    from_pattern = re.compile(r'FROM\s+(\w+)(?=\s+JOIN|\s+WHERE|$)', re.IGNORECASE)
    join_pattern = re.compile(r'JOIN\s+(.*?)(?=\s+JOIN|\s+WHERE|$)', re.IGNORECASE)
    where_pattern = re.compile(r'WHERE\s+(.+)(?=\sORDER)', re.IGNORECASE)
    order_by_pattern = re.compile(r'ORDER\s+BY\s+(.+)', re.IGNORECASE)
    and_or_pattern = re.compile(r'\bAND\b|\bOR\b', re.IGNORECASE)
    def __init__(self, sql_query):
        self.sql_query = ' '.join(line.strip() for line in sql_query.splitlines()).strip()
        self.select_columns = []
        self.from_table = ''
        self.joins = []
        self.where_conditions = []
        self.order_by = []
        self.parse_query()

    def parse_query(self):
        self.parse_select()
        self.parse_from()
        self.parse_join()
        self.parse_where()
        self.parse_order_by()

    def parse_select(self):
        select_match = self.select_pattern.search(self.sql_query)
        if select_match:
            self.select_columns = [col.strip() for col in select_match.group(1).split(',')]

    def parse_from(self):
        from_match = self.from_pattern.search(self.sql_query)
        if from_match:
            self.from_table = from_match.group(1).strip()
            # if from_match.group(2):
            #     self.from_table += f' AS {from_match.group(2).strip()}'

    def parse_join(self):
        join_matches = self.join_pattern.findall(self.sql_query)
        if not join_matches:
            return
        for join_match in join_matches:
            res = dict()
            fr = join_match.split("ON")
            res['table']=fr[0].strip()
            res['conditions']=[f.strip() for f in self.and_or_pattern.split(fr[1])]
            self.joins.append(res)

    def parse_where(self):
        where_match = self.where_pattern.search(self.sql_query)
        print(where_match)
        if where_match:
            self.where_conditions = [cond.strip() for cond in self.and_or_pattern.split(where_match.group(1))]

    def parse_order_by(self):
        order_by_match = self.order_by_pattern.search(self.sql_query)
        if order_by_match:
            self.order_by = [col.strip() for col in order_by_match.group(1).split(',')]

    def to_json(self):
        result = {}
        if self.select_columns:
            result['select'] = self.select_columns
        if self.from_table:
            result['from'] = self.from_table
        if self.joins:
            result['joins'] = self.joins
        if self.where_conditions:
            result['where'] = self.where_conditions
        if self.order_by:
            result['order_by'] = self.order_by
        result['full_query'] = self.sql_query
        result['creation_timestamp'] = datetime.now().isoformat()
        return result