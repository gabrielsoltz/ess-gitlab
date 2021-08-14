#!/usr/bin/env python3

import gitlab
import argparse
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
    dict = {project_id: [
            get_project_info(gl, project_id),
            check_project_visbility(gl, project_id),
            check_project_pages_access_level(gl, project_id),
            check_project_security_and_compliance_enabled(gl, project_id),
            check_project_approvals_before_merge(gl, project_id),
            check_project_push_rules_unsigned_commits(gl, project_id),
            check_project_push_rules_comitter_check(gl, project_id)
        ]
    }
    return dict

def check_all_projects(gl):
    dict = {}
    projects = get_all_projects(gl)
    for project in projects:
        dict_projcet = check_project(gl, project.id)
        dict.update(dict_projcet)
    return dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gitlab Audit')

    parser.add_argument('--gitlab_url', help="Gitlab URL", required=True)
    parser.add_argument('--gitlab_token', help="Gitlab Token", required=True)

    parser.add_argument('--check', help="Type of check (project)", required=True)
    parser.add_argument('--project_id', help="Project ID", required=True)

    args = vars(parser.parse_args())
    gitlab_url = args["gitlab_url"]
    gitlab_token = args["gitlab_token"]
    project_id = args["project_id"]
    check = args["check"]

    gl = connect(gitlab_url, gitlab_token)

    if check == 'project':
        if project_id == "all": 
            output = check_all_projects(gl)
            projects_dict_output = {'projects': output}
        else:
            try:
                int(project_id)
                output = check_project(gl, project_id)
                projects_dict_output = {'projects': output}
            except:
                print ("Project Select error")
    
    scan = {'easyscan-gitlab': projects_dict_output}
    print (scan)
            