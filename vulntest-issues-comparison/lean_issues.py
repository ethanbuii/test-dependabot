import sys
import json
import argparse
import argcomplete

required_fields=['id', 'self', 'key', 'fields.statusCategory', 'fields.customfield_10184',
    'fields.reporter', 'fields.customfield_10346', 'fields.priority', 'fields.status', 'fields.customfield_10183']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Lean the issues list")
    
    parser.add_argument('--input', type = str, required=True, help='Missing path args')
    parser.add_argument('--output', type = str, required=True, help='Missing path args')
    
    argcomplete.autocomplete(parser)
    
    args = parser.parse_args()
    file = open(args.input, 'r')
    issues = json.loads(file.buffer.read())
    
    leaned_issues = []
    for issue in issues:
        obj = {}
        for field in required_fields:
            sub_field = field.split('.')
            if len(sub_field) == 1 and sub_field[0] in issue:
               obj[sub_field[0]] = issue.get(sub_field[0])
            # contains nested field
            else:
                obj[field] = issue.get(sub_field[0]).get(sub_field[1])
        leaned_issues.append(obj)
    
    writer = open(args.output, 'w')
    writer.write(json.dumps(leaned_issues))