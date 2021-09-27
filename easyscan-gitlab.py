#!/usr/bin/env python3

import gitlab
import argparse
import json
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
    dict.update(get_project_all_keys(gl, project_id))
    dict.update(check_project_pipeline(gl, project_id))
    dict.update(check_project_codeowners(gl, project_id))
    project_dict = {project_id: dict}
    return project_dict

def check_baseline(baseline_file, scan):
    baseline_output = {}
    with open(baseline_file, 'r') as stream:
        try:
            baseline_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
        for category, ids in baseline_yaml.items():
            baseline_id_output = {}
            for id_dict in ids:
                for id, values in id_dict.items():
                    baseline_check_output = {}
                    for value in values:
                        for check, expected in value.items():
                            print('Expected for ', check, 'is', expected)
                            if expected:
                                result = scan['easyscan-gitlab'][category][str(id)][check]
                                if expected == result:
                                    baseline_check_output.update({check: 'PASS'})
                                    print ('TRUE')
                                else:
                                    baseline_check_output.update({check: 'FAIL'})
                                    print('FALSE')
            baseline_id_output.update({id: baseline_check_output})
        baseline_output.update({category: baseline_id_output})
    return baseline_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gitlab Audit')

    parser.add_argument('--gitlab_url', help="Gitlab URL", required=True)
    parser.add_argument('--gitlab_token', help="Gitlab Token", required=True)

    parser.add_argument('--mode', help="Inventory or Baseline", required=True)

    parser.add_argument('--check', help="Type of check (project)", required=True)
    parser.add_argument('--id', help="Gitlab Project/Group ID", required=True)

    args = vars(parser.parse_args())
    gitlab_url = args["gitlab_url"]
    gitlab_token = args["gitlab_token"]
    mode = args["mode"]
    id = args["id"]
    check = args["check"]

    gl = connect(gitlab_url, gitlab_token)
 
    if check == 'project':
        projects = get_project_ids(gl, id)
        project_output = {}
        for project in projects:
            dict_project = check_project(gl, project)
            project_output.update(dict_project)
        projects_dict_output = {'projects': project_output}

    scan = {'easyscan-gitlab': projects_dict_output}
    if mode == 'baseline':
        baseline_output = {'baseline': check_baseline('baselines/default.yml', scan)}
        output = {'easyscan-gitlab': baseline_output}
        print(json.dumps(output, indent=4, sort_keys=True))
    if mode == 'inventory':
        print(json.dumps(scan, indent=4, sort_keys=True))