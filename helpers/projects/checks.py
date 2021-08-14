from gitlab import exceptions
from helpers.projects.methods import *

def check_project_visbility(gl, project_id):
    try:
        attributes = get_project_attributes(gl, project_id)
    except exceptions.GitlabGetError:
        return {'check_project_visbility': '403 Forbidden'}
    return {'check_project_visbility': attributes['visibility']}

def check_project_pages_access_level(gl, project_id):
    try:
        attributes = get_project_attributes(gl, project_id)
    except exceptions.GitlabGetError:
        return {'check_project_visbility': '403 Forbidden'}
    return {'check_project_pages_access_level': attributes['pages_access_level']}

def check_project_security_and_compliance_enabled(gl, project_id):
    try:
        attributes = get_project_attributes(gl, project_id)
    except exceptions.GitlabGetError:
        return {'check_project_visbility': '403 Forbidden'}
    return {'check_project_security_and_compliance_enabled': attributes['security_and_compliance_enabled']}

def check_project_approvals_before_merge(gl, project_id):
    try:
        attributes = get_project_attributes(gl, project_id)
    except exceptions.GitlabGetError:
        return {'check_project_visbility': '403 Forbidden'}
    return {'check_project_approvals_before_merge': attributes['approvals_before_merge']}

def check_project_push_rules_unsigned_commits(gl, project_id):
    try:
        push_rules = get_project_push_rules(gl, project_id)
    except exceptions.GitlabGetError:
        return {'check_project_visbility': '403 Forbidden'}
    return {'check_project_push_rules_unsigned_commits': push_rules.reject_unsigned_commits}

def check_project_push_rules_comitter_check(gl, project_id):
    #Committer restriction: Users can only push commits to this repository that were committed with one of their own verified emails.
    try:
        push_rules = get_project_push_rules(gl, project_id)
    except exceptions.GitlabGetError:
        return {'check_project_visbility': '403 Forbidden'}
    return {'check_project_push_rules_comitter_check': push_rules.commit_committer_check}

def get_project_info(gl, project_id):
    try:
        attributes = get_project_attributes(gl, project_id)
    except exceptions.GitlabGetError:
        return {'project_info': '403 Forbidden'}
    return {'project_info': {'name': attributes['name'], 'name_with_namespace': attributes['name_with_namespace'], 'description': attributes['description'], 'web_url': attributes['web_url']}}