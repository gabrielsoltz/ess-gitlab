#!/usr/bin/env python3

import gitlab
import argparse
import json
import pyfiglet
import logging
import sys, os

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
    ascii_banner = pyfiglet.figlet_format("EasyScan Gitlab")
    print (ascii_banner)
    print ('Gitlab URL:', gitlab_url)
    print ('Mode:', mode)
    print ('Check:', check)
    print ('Json File:', jsonfile)
    print ('Log Level:', log_level)
    print ('Baseline File:', baseline_file)

def check_project(gl, project_id):
    dict = {}
    dict.update(get_project_info(gl, project_id))
    dict.update(check_project_visibility(gl, project_id))
    dict.update(check_project_pages_access_level(gl, project_id))
    dict.update(check_project_security_and_compliance_enabled(gl, project_id))
    dict.update(check_project_approvals_before_merge(gl, project_id))
    dict.update(check_project_push_rules_unsigned_commits(gl, project_id))
    dict.update(check_project_push_rules_comitter_check(gl, project_id))
    dict.update(check_project_protected_branches(gl, project_id))
    dict.update(check_project_access_tokens(gl, project_id))
    dict.update(check_project_deploy_tokens(gl, project_id))
    dict.update(check_project_deploy_keys(gl, project_id))
    dict.update(check_project_pipeline(gl, project_id))
    dict.update(check_project_pipeline_stages(gl, project_id))
    dict.update(check_project_pipeline_images(gl, project_id))
    dict.update(check_project_codeowners(gl, project_id))
    project_dict = {project_id: dict}
    return project_dict

def check_baseline_items(expected, result):
    try:
        result = result.lstrip()
    except:
        result = result
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
                                for scans_id in scan['easyscan-gitlab'][category]:
                                    if not scans_id in baseline_output_by_check_id:
                                        baseline_output_by_check_id[scans_id] = []
                                    baseline_output_by_check = {}
                                    logging.info('ProjectID: ' + str(scans_id) + ' | Check: ' + str(check) + ' | Expected: ' + str(expected) + ' | Type: ' + str(type(expected)) + ' | Result: ' + str(scan['easyscan-gitlab'][category][scans_id][check]))
                                    if expected != 'None' and expected is not None:
                                        result = scan['easyscan-gitlab'][category][scans_id][check]
                                        if check_baseline_items(expected, result):
                                            baseline_output_by_check.update({check: 'PASS'})
                                        else:
                                            baseline_output_by_check.update({check: 'FAIL'})
                                        baseline_output_by_check_id[scans_id].append(baseline_output_by_check)
                            elif int(id) in scan['easyscan-gitlab'][category]:
                                logging.info('Checking Baseline: ' + str(id))
                                if not id in baseline_output_by_check_id:
                                    baseline_output_by_check_id[id] = []
                                baseline_output_by_check = {}
                                logging.info('ProjectID: ' + str(id) + ' | Check: ' + str(check) + ' | Expected: ' + str(expected) + ' | Type: ' + str(type(expected)) + ' | Result: ' + str(scan['easyscan-gitlab'][category][id][check]))
                                if expected != 'None' and expected is not None:
                                    result = scan['easyscan-gitlab'][category][int(id)][check]
                                    if check_baseline_items(expected, result):
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
    total_checks = 0
    for projects, findings in baseline['easyscan-gitlab']['baseline']['projects'].items():
        total_projects += 1
        total_fails_by_project = 0
        total_pass_by_project = 0
        total_checks_by_project = 0
        for finding in findings:
            for check, value in finding.items():
                total_checks += 1
                total_checks_by_project += 1
                if value == 'FAIL':
                    total_fails += 1
                    total_fails_by_project += 1
                elif value == 'PASS':
                    total_pass += 1
                    total_pass_by_project += 1
        print ('Project:', projects, '| FAILS:', total_fails_by_project, '| PASS:', total_pass_by_project, '| Checks: ', total_checks_by_project)
    print ('Total Projects:', total_projects, '| Total FAILS:', total_fails, '| Total PASS:', total_pass, '| Total Checks: ', total_checks)

def write_json(content, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description='''
    EasyScan Gitlab (Easy Scanning for Gitlab Mis-Configurations)
    https://github.com/gabrielsoltz/easyscan-gitlab
    Author: Gabriel Soltz
    '''
    )

    parser.add_argument('-u', '--gitlab_url', help="Gitlab URL", required=True)
    parser.add_argument('-t', '--gitlab_token', help="Gitlab Token", required=False)
    parser.add_argument('-m', '--mode', help="Inventory or Baseline", required=True)
    parser.add_argument('-c', '--check', help="Type of check (project)", required=True)
    parser.add_argument('-i', '--id', help="Gitlab Project/Group ID", required=True)
    parser.add_argument('-j', '--jsonfile', default="True", help="Write JSON Output (True/False)", required=False)
    parser.add_argument('-l', '--log', default="ERROR", help="Log Level (Default: ERROR) (Valid Options: ERROR, INFO or DEBUG)" , required=False)
    parser.add_argument('-b', '--baseline', default="baselines/default.yml", help="Baseline File (Default: baselines/default.yml)", required=False)

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
    check = args["check"]
    id = args["id"]
    jsonfile = args["jsonfile"]
    log_level = args["log"]
    if log_level == 'ERROR':
        logging.basicConfig(level=logging.ERROR)
    elif log_level == 'INFO':
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)
    baseline_file = args["baseline"]

    banner()

    gl = connect(gitlab_url, gitlab_token)
 
    if check == 'project':
        projects, id_type = get_project_ids(gl, id)
        print ('ID Type:', id_type)
        project_output = {}
        for project in projects:
            dict_project = check_project(gl, project)
            project_output.update(dict_project)
        projects_dict_output = {'projects': project_output}
        inventory = {'easyscan-gitlab': projects_dict_output}
        
    if mode == 'baseline':
        baseline_output = {'baseline': check_baseline(baseline_file, inventory)}
        baseline = {'easyscan-gitlab': baseline_output}
        print(json.dumps(baseline, indent=4, sort_keys=True))
        if jsonfile:
            write_json(baseline, 'baseline-' + id + '.json')
        check_baseline_statistics(baseline)
    if mode == 'inventory':
        print(json.dumps(inventory, indent=4, sort_keys=True))
        if jsonfile:
            write_json(baseline, 'invetory-' + id + '.json')
    
    