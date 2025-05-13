import json
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="check the issues on main branch")
    
    parser.add_argument('--main-issue', required=True, type=str, help='issue file path')
    parser.add_argument('--none-main-issue', required=True, type=str, help='issue file path')
    
    args = parser.parse_args()
    file = open(args.main_issue, 'r')
    
    main_issues = json.loads(file.buffer.read())
    # print(len(main_issues))
    file.close()
    file = open(args.none_main_issue)
    none_main_issues = json.loads(file.buffer.read())
    # print(len(none_main_issues))
    file.close()
    # print(main_issues)
    only_main_issues=[]
    
    for mi in main_issues:
        cve_id = mi.get('fields').get('customfield_10183')
        nmi = next((issue for issue in none_main_issues if (
            # cve-id
            issue.get('fields').get('customfield_10183') == cve_id
            # docker image
            and issue.get('fields').get('customfield_10346') == mi.get('fields').get('customfield_10346')
            )), None)
        if nmi is None:
            only_main_issues.append(mi)
            continue
        else:
            # severity
            if (nmi.get('fields').get('customfield_10184').get('value') != mi.get('fields').get('customfield_10184').get('value') 
                # docker image
                or nmi.get('fields').get('customfield_10346') != mi.get('fields').get('customfield_10346') 
                # issue's status
                or nmi.get('fields').get('status').get('name') != mi.get('fields').get('status').get('name')
                # priority
                or nmi.get('fields').get('priority').get('name') != mi.get('fields').get('priority').get('name')):
                only_main_issues.append(mi)
    
            # only_main_issues.append(mi)
    # print(len(only_main_issues))
    
    print(len(only_main_issues))
    file = open('only-main-issues.json', 'w')
    file.write(json.dumps(only_main_issues))