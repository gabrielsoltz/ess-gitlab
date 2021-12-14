#!/usr/bin/env python3

import gitlab
import argparse
import json
import pyfiglet
import logging
import sys, os

from helpers.projects.service import GitlabGroupService, GitlabProjectService
from helpers.projects.checks import *

def connect(gitlab_url, gitlab_token):
    type='gitlab_token'
    if type == 'gitlab_token':
        # private token or personal token authentication
        gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)
        return gl

    # oauth token authentication
    #gl = gitlab.Gitlab('http://10.0.0.1', oauth_token='my_long_token_here')

    # job token authentication (to be used in CI)
    #import os
    #gl = gitlab.Gitlab('http://10.0.0.1', job_token=os.environ['CI_JOB_TOKEN'])

    # anonymous gitlab instance, read-only for public resources
    #gl = gitlab.Gitlab('http://10.0.0.1')

    # Define your own custom user agent for requests
    #gl = gitlab.Gitlab('http://10.0.0.1', user_agent='my-package/1.0.0')

    # make an API request to create the gl.user object. This is mandatory if you
    # use the username/password authentication.
    #gl.auth()

def banner():
    ascii_banner = pyfiglet.figlet_format("ESS-Gitlab")
    print (ascii_banner)
    print ('------------------------')
    print ('Gitlab URL:', gitlab_url)
    print ('Mode:', mode)
    print ('Check:', check)
    print ('Json File:', jsonfile)
    print ('Log Level:', log_level)
    print ('Baseline File:', baseline_file)
    print ('Total Only:', totalonly)
    print ('Scan Archived:', scan_archived)
    print ('Maximun projects when using all:', max_all)
    print ('------------------------')

def check_project(gl_project):
    dict = {}
    dict.update(gl_project.project_info)
    dict.update(check_project_visibility(gl_project))
    dict.update(check_project_pages_access_level(gl_project))
    dict.update(check_project_security_and_compliance_enabled(gl_project))
    dict.update(check_project_approvals_before_merge(gl_project))
    dict.update(check_project_push_rules_unsigned_commits(gl_project))
    dict.update(check_project_push_rules_comitter_check(gl_project))
    dict.update(check_project_protected_branches(gl_project))
    dict.update(check_project_access_tokens(gl_project))
    dict.update(check_project_deploy_tokens(gl_project))
    dict.update(check_project_deploy_keys(gl_project))
    dict.update(check_project_pipeline(gl_project))
    dict.update(check_project_pipeline_stages(gl_project))
    dict.update(check_project_pipeline_images(gl_project))
    dict.update(check_project_codeowners(gl_project))
    dict.update(check_project_shared_runners_enabled(gl_project))
    dict.update(check_project_runners(gl_project))
    dict.update(check_project_runners_shared(gl_project))
    dict.update(check_project_runners_notshared(gl_project))
    if scanlog4j:
        dict.update(check_project_log4j(gl_project))
    project_dict = {gl_project.project_id: dict}
    return project_dict

def check_baseline_items(expected, result):
    try:
        result = result.lstrip()
    except:
        result = result
    if result == 'ERROR':
        logging.info('Str: ERROR')
        return 'ERROR'
    if isinstance(expected, list):
        for i in expected:
            found = False
            if result:
                if i in result:
                    logging.info('List: Matched 1 list element')
                    return True
            elif not result:
                logging.info('List: No matched list elements')
                return False
        if not expected and result:
            logging.info('List: No elements in list but result found')
            return False
        elif not found and result:
            logging.info('List: Elements in List but not matched')
            return False
    if isinstance(expected, str):
        if expected == result:
            logging.info('Str: Matched')
            return True
        else:
            logging.info('Str: Not Matched')
            return False
    if isinstance(expected, bool):
        if expected == result:
            logging.info('Bool: Matched as ==')
            return True
        elif expected and result:
            logging.info('Bool: Matched as True')
            return True
        elif not expected and not result: 
            logging.info('Bool: Matched as False')
            return True
        else:
            logging.info('Bool: Not Matched')
            return False
    if isinstance(expected, int):
        if expected == result:
            logging.info('Int: Matched')
            return True
        else:
            logging.info('Int: Not matched')
            return False

def check_baseline(baseline_file, scan):
    baseline_output = {}
    with open(baseline_file, 'r') as stream:
        try:
            baseline_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
        for category, ids in baseline_yaml.items():
            baseline_output_by_check_id = {}
            for id_dict in ids:
                for id, values in id_dict.items():
                    for value in values:
                        for check, expected in value.items():
                            try:
                                expected = expected.lstrip()
                            except:
                                expected = expected
                            if str(id) == '*':
                                logging.info('Checking Baseline: ' + str(id))
                                for scans_id in scan['ess-gitlab'][category]:
                                    try:
                                        project_name = scan['ess-gitlab'][category][scans_id]['project_info']['name_with_namespace']
                                    except: 
                                        project_name = scan['ess-gitlab'][category][scans_id]['project_info']
                                        logging.error('ProjectID: ' + str(scans_id) + ' | project_name error: ' + project_name)
                                    try:
                                        project_url = scan['ess-gitlab'][category][scans_id]['project_info']['web_url']
                                    except:
                                        project_url = scan['ess-gitlab'][category][scans_id]['project_info']
                                        logging.error('ProjectID: ' + str(scans_id) + ' | project_url error: ' + project_url)
                                    if not scans_id in baseline_output_by_check_id:
                                        baseline_output_by_check_id[scans_id] = []
                                        baseline_output_by_check_id[scans_id].append({'name': project_name})
                                        baseline_output_by_check_id[scans_id].append({'url': project_url})
                                    baseline_output_by_check = {}
                                    logging.info('ProjectID: ' + str(scans_id) + ' | Check: ' + str(check) + ' | Expected: ' + str(expected) + ' | Type: ' + str(type(expected)) + ' | Result: ' + str(scan['ess-gitlab'][category][scans_id][check]))
                                    if expected != 'None' and expected is not None:
                                        result = scan['ess-gitlab'][category][scans_id][check]
                                        if check_baseline_items(expected, result) == 'ERROR':
                                            baseline_output_by_check.update({check: 'ERROR'})
                                        elif check_baseline_items(expected, result):
                                            baseline_output_by_check.update({check: 'PASS'})
                                        else:
                                            baseline_output_by_check.update({check: 'FAIL'})
                                        baseline_output_by_check_id[scans_id].append(baseline_output_by_check)
                            elif str(id) in scan['ess-gitlab'][category]:
                                logging.info('Checking Baseline: ' + str(id))
                                try:
                                    project_name = scan['ess-gitlab'][category][str(id)]['project_info']['name_with_namespace']
                                except: 
                                    project_name = scan['ess-gitlab'][category][str(id)]['project_info']
                                    logging.error('ProjectID: ' + str(scans_id) + ' | project_name error: ' + project_name)
                                try:
                                    project_url = scan['ess-gitlab'][category][str(id)]['project_info']['web_url']
                                except:
                                    project_url = scan['ess-gitlab'][category][str(id)]['project_info']
                                    logging.error('ProjectID: ' + str(scans_id) + ' | project_url error: ' + project_url)
                                if not id in baseline_output_by_check_id:
                                    baseline_output_by_check_id[id] = []
                                    baseline_output_by_check_id[id].append({'name': project_name})
                                    baseline_output_by_check_id[id].append({'url': project_url})
                                baseline_output_by_check = {}
                                logging.info('ProjectID: ' + str(id) + ' | Check: ' + str(check) + ' | Expected: ' + str(expected) + ' | Type: ' + str(type(expected)) + ' | Result: ' + str(scan['ess-gitlab'][category][str(id)][check]))
                                if expected != 'None' and expected is not None:
                                    result = scan['ess-gitlab'][category][str(id)][check]
                                    if check_baseline_items(expected, result) == 'ERROR':
                                        baseline_output_by_check.update({check: 'ERROR'})
                                    elif check_baseline_items(expected, result):
                                        baseline_output_by_check.update({check: 'PASS'})
                                    else:
                                        baseline_output_by_check.update({check: 'FAIL'})
                                    baseline_output_by_check_id[id].append(baseline_output_by_check)
            baseline_output.update({category: baseline_output_by_check_id})
    return baseline_output

def check_baseline_statistics(baseline):
    print ('--------------- STATISTICS ---------------')
    total_projects = 0 
    total_fails = 0
    total_pass = 0
    total_errors = 0
    total_checks = 0
    for projects, findings in baseline['ess-gitlab']['baseline']['projects'].items():
        total_projects += 1
        total_fails_by_project = 0
        total_pass_by_project = 0
        total_errors_by_project = 0
        total_checks_by_project = 0
        for finding in findings:
            for check, value in finding.items():
                if check == 'name' or check == 'url':
                    if check == 'name':
                        name = value
                    if check == 'url':
                        url = value
                else:
                    total_checks += 1
                    total_checks_by_project += 1
                    if value == 'FAIL':
                        total_fails += 1
                        total_fails_by_project += 1
                    elif value == 'PASS':
                        total_pass += 1
                        total_pass_by_project += 1
                    elif value == 'ERROR':
                        total_errors += 1
                        total_errors_by_project += 1
        if not totalonly:
            print ('Project:', name, ' (', projects, ')', '| FAILS:', total_fails_by_project, '| PASS:', total_pass_by_project, '| ERRORS:', total_errors_by_project, '| Checks: ', total_checks_by_project)
    print ('Total Projects:', total_projects, '| Total FAILS:', total_fails, '| Total PASS:', total_pass, '| Total Errors:', total_errors, '| Total Checks: ', total_checks)
    
def write_json(content, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description='''
    ESS-Gitlab (EasyScan Security Gitlab)
    https://github.com/gabrielsoltz/ess-gitlab
    Author: Gabriel Soltz
    '''
    )

    parser.add_argument('-u', '--gitlab_url', help="Gitlab URL", required=True)
    parser.add_argument('-t', '--gitlab_token', help="Gitlab Token", required=False)
    parser.add_argument('-m', '--mode', help="Inventory or Baseline", required=True)
    parser.add_argument('-c', '--check', help="Type of check (project)", required=True)
    parser.add_argument('-i', '--id', nargs = '*', help="Gitlab Project ID or Group ID or all, use spaces to add more than 1", required=True)
    parser.add_argument('-j', '--jsonfile', action=argparse.BooleanOptionalAction, help="Write JSON Output", required=False)
    parser.add_argument('-p', '--jsonprint', action=argparse.BooleanOptionalAction, help="Show JSON Output", required=False)
    parser.add_argument('-l', '--log', default="ERROR", help="Log Level (Default: ERROR) (Valid Options: ERROR, INFO or DEBUG)" , required=False)
    parser.add_argument('-b', '--baseline', default="baselines/default.yml", help="Baseline File (Default: baselines/default.yml)", required=False)
    parser.add_argument('-to', '--totalonly', action="store_true", help="Show total only (Default: No)", required=False)
    parser.add_argument('-a', '--scan-archived', action="store_true", help="Include archived projects (Default: No)", required=False)
    parser.add_argument('-ma', '--max-all', default=100, help="Maximun amount of projects when using all as id (Default: 100)", required=False)
    parser.add_argument('--scanlog4j', action=argparse.BooleanOptionalAction, help="Scan Log4J", required=False)

    args = vars(parser.parse_args())
    gitlab_url = args["gitlab_url"]
    if args["gitlab_token"]:
        gitlab_token = args["gitlab_token"]
    else:
        # Use environment variable
        gitlab_token = os.environ.get("gitlab_token")
        if gitlab_token == None:
            logging.error("ERROR: No token found in environment, please check existence of 'gitlab_token' in current environment!")
            sys.exit(1)

    mode = args["mode"]
    available_modes = ('baseline', 'inventory')
    if mode not in available_modes:
        logging.error("ERROR: Wrong mode. Use: {}".format(",".join(map(str,available_modes))))
        sys.exit(1)

    check = args["check"]
    available_checks = ('project', )
    if check not in available_checks:
        logging.error("ERROR: Wrong check. Use: {}".format(",".join(map(str,available_checks))))
        sys.exit(1)

    ids = args["id"]

    jsonfile = True
    if not args["jsonfile"]:
        jsonfile = False

    jsonprint = True
    if not args["jsonprint"]:
        jsonprint = False

    log_level = args["log"]
    if log_level == 'ERROR':
        logging.basicConfig(level=logging.ERROR)
    elif log_level == 'INFO':
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)
    
    baseline_file = args["baseline"]
    totalonly = args["totalonly"]
    scan_archived = args["scan_archived"]    
    max_all = int(args["max_all"])

    scanlog4j = True
    if not args["scanlog4j"]:
        scanlog4j = False

    banner()

    gl = connect(gitlab_url, gitlab_token)
 
    if check == 'project':
        project_output = {}
        project_archived_output = {}
        count_archived_all = 0
        for id in ids:
            gl_group = GitlabGroupService(gl, id, logging, max_all)
            print ('ID:', gl_group.group_id)
            print ('ID Type:', gl_group.group_type)
            print ('Projects #: ', gl_group.projects_len)
            count = 0
            count_archived = 0
            for project in gl_group.projects_ids:
                count += 1
                print('Scanning Project:', project, str(count) + "/" + str(gl_group.projects_len) + "... ")
                gl_project = GitlabProjectService(gl, project, logging)
                if not gl_project.project_archived:
                    dict_project = check_project(gl_project)
                    project_output.update(dict_project)
                else:
                    if scan_archived:
                        dict_project = check_project(gl_project)
                        project_output.update(dict_project)
                    else:
                        dict_project = {gl_project.project_id: ''}
                    project_archived_output.update(dict_project)
                    count_archived += 1
                    count_archived_all += 1
                    logging.info('Project Archived:', project)
        print('Archived Projects', count_archived_all)
        projects_dict_output = {'projects': project_output}
        inventory = {'ess-gitlab': projects_dict_output}
        
    if mode == 'baseline':
        baseline_output = {'baseline': check_baseline(baseline_file, inventory)}
        baseline = {'ess-gitlab': baseline_output}
        if jsonprint:
            print(json.dumps(baseline, indent=4, sort_keys=True))
        else:
            print("not dumped JSON")
        if jsonfile:
            write_json(baseline, 'baseline-' + '-'.join(ids) + '.json')
        else:
            print("Not writing JSON files")
        check_baseline_statistics(baseline)
    if mode == 'inventory':
        print(json.dumps(inventory, indent=4, sort_keys=True))
        if jsonfile:
            write_json(inventory, 'invetory-' + '-'.join(ids) + '.json')