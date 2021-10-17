from gitlab import exceptions
from helpers.projects.service import *


def get_project_info(gl, project_id):
    try:
        attributes = get_project_attributes(gl, project_id)
        project_languages = get_project_languages(gl, project_id)
        project_contributors = get_project_contributors(gl, project_id)
    except exceptions.GitlabGetError:
        return {'project_info': '403 Forbidden'}
    return {'project_info': {'name': attributes['name'], 'name_with_namespace': attributes['name_with_namespace'], 'description': attributes['description'], 'web_url': attributes['web_url'], 'project_languages': project_languages, 'project_contributors': project_contributors}}

def check_project_visibility(gl, project_id):
    try:
        attributes = get_project_attributes(gl, project_id)
    except exceptions.GitlabGetError:
        return {'project_visibility': '403 Forbidden'}
    return {'project_visibility': attributes['visibility']}

def check_project_pages_access_level(gl, project_id):
    try:
        attributes = get_project_attributes(gl, project_id)
    except exceptions.GitlabGetError:
        return {'project_pages_access_level': '403 Forbidden'}
    return {'project_pages_access_level': attributes['pages_access_level']}

def check_project_security_and_compliance_enabled(gl, project_id):
    try:
        attributes = get_project_attributes(gl, project_id)
    except exceptions.GitlabGetError:
        return {'project_security_and_compliance_enabled': '403 Forbidden'}
    return {'project_security_and_compliance_enabled': attributes['security_and_compliance_enabled']}

def check_project_approvals_before_merge(gl, project_id):
    try:
        attributes = get_project_attributes(gl, project_id)
    except exceptions.GitlabGetError:
        return {'project_approvals_before_merge': '403 Forbidden'}
    return {'project_approvals_before_merge': attributes['approvals_before_merge']}

def check_project_push_rules_unsigned_commits(gl, project_id):
    try:
        push_rules = get_project_push_rules(gl, project_id)
    except exceptions.GitlabGetError:
        return {'project_push_rules_unsigned_commits': '403 Forbidden'}
    return {'project_push_rules_unsigned_commits': push_rules.reject_unsigned_commits}

def check_project_push_rules_comitter_check(gl, project_id):
    #Committer restriction: Users can only push commits to this repository that were committed with one of their own verified emails.
    try:
        push_rules = get_project_push_rules(gl, project_id)
    except exceptions.GitlabGetError:
        return {'project_push_rules_comitter_check': '403 Forbidden'}
    return {'project_push_rules_comitter_check': push_rules.commit_committer_check}

def check_project_protected_branches(gl, project_id):
    try:
        protected_branches = get_protectedbranches(gl, project_id)
    except exceptions.GitlabGetError:
        return {'project_protected_branches': '403 Forbidden'}
    except exceptions.GitlabListError:
        return {'project_protected_branches': '403 Forbidden'}
    for i in protected_branches:
        protected_branches = i
    try:
        return {'project_protected_branches': protected_branches._attrs}
    except:
        return {'project_protected_branches': protected_branches}

def check_project_access_tokens(gl, project_id):
    try:
        access_tokens = get_project_access_tokens(gl, project_id)
        for i in access_tokens:
            access_tokens = i
        try:
            return {'project_access_tokens': access_tokens._attrs}
        except:
            return {'project_access_tokens': access_tokens}
    except exceptions.GitlabGetError:
        return {'project_access_tokens': '403 Forbidden'}
    except exceptions.GitlabAuthenticationError:
        return {'project_access_tokens': '401 Unauthorized'}


def check_project_deploy_tokens(gl, project_id):
    try:
        project_deploy_tokens = get_project_deployment_tokens(gl, project_id)
        for i in project_deploy_tokens:
            project_deploy_tokens = i
        try:
            return {'project_deploy_tokens': project_deploy_tokens._attrs}
        except:
            return {'project_deploy_tokens': project_deploy_tokens}
    except exceptions.GitlabGetError:
        return {'project_deploy_tokens': '403 Forbidden'}
    except exceptions.GitlabAuthenticationError:
        return {'project_deploy_tokens': '401 Unauthorized'}
    except exceptions.GitlabListError:
        return {'project_deploy_tokens': '403 Forbidden'}

def check_project_deploy_keys(gl, project_id):
    try:
        project_deploy_keys = get_project_keys(gl, project_id)
        for i in project_deploy_keys:
            project_deploy_keys = i
        try:
            return {'project_deploy_keys': project_deploy_keys._attrs}
        except:
            return {'project_deploy_keys': project_deploy_keys}
    except exceptions.GitlabGetError:
        return {'project_deploy_keys': '403 Forbidden'}
    except exceptions.GitlabAuthenticationError:
        return {'project_deploy_keys': '401 Unauthorized'}
    except exceptions.GitlabListError:
        return {'project_deploy_keys': '403 Forbidden'}

def check_project_pipeline(gl, project_id):
    try:
        pipeline_file = get_project_file(gl, project_id, '.gitlab-ci.yml')
    except exceptions.GitlabGetError:
        return {'project_pipeline': False}
    return {'project_pipeline': True}

def check_project_pipeline_stages(gl, project_id):
    try:
        pipeline_file = get_project_file(gl, project_id, '.gitlab-ci.yml')
    except exceptions.GitlabGetError:
        return {'project_pipeline_stages': False}
    pipeline_block_stages = get_project_pipeline_block(pipeline_file, 'stages')
    return pipeline_block_stages

def check_project_pipeline_images(gl, project_id):
    try:
        pipeline_file = get_project_file(gl, project_id, '.gitlab-ci.yml')
    except exceptions.GitlabGetError:
        return {'project_pipeline_image': False}
    pipeline_block_images = get_project_pipeline_content_of_block(pipeline_file, 'image')
    return pipeline_block_images

def check_project_codeowners(gl, project_id):
    try:
        codeowners_file = get_project_file(gl, project_id, 'CODEOWNERS')
        return {'project_codeowners': codeowners_file}
    except exceptions.GitlabGetError:
        return {'project_codeowners': False}
    
def check_project_shared_runners_enabled(gl, project_id):
    try:
        shared_runners_enabled = get_project_shared_runners_enabled(gl, project_id)
    except exceptions.GitlabGetError:
        return {'project_shared_runners_enabled': '403 Forbidden'}
    return {'project_shared_runners_enabled': shared_runners_enabled}

def check_project_runners(gl, project_id):
    try:
        project_runners = get_project_runners(gl, project_id)
        project_runners_list = []
        for i in project_runners:
            project_runners = i
            try:
                project_runners = project_runners._attrs
            except:
                project_runners = project_runners
            project_runners_list.append(project_runners)
        try:
            return {'project_runners': project_runners_list}
        except:
            return {'project_runners': project_runners_list}
    except exceptions.GitlabGetError:
        return {'project_runners': '403 Forbidden'}
    except exceptions.GitlabAuthenticationError:
        return {'project_runners': '401 Unauthorized'}
    except exceptions.GitlabListError:
        return {'project_runners': '403 Forbidden'}