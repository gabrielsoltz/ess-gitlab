from helpers.projects.service import *


def check_project_visibility(project):
    if project.project_attributes is not None:
        return {'project_visibility': project.project_attributes['visibility']}
    return {'project_visibility': 'ERROR'}

def check_project_pages_access_level(project):
    if project.project_attributes is not None:
        return {'project_pages_access_level': project.project_attributes['pages_access_level']}
    return {'project_pages_access_level': 'ERROR'}

def check_project_security_and_compliance_enabled(project):
    if project.project_attributes is not None:
        return {'project_security_and_compliance_enabled': project.project_attributes['security_and_compliance_enabled']}
    return {'project_security_and_compliance_enabled': 'ERROR'}

def check_project_approvals_before_merge(project):
    if project.project_attributes is not None:
        return {'project_approvals_before_merge': project.project_attributes['approvals_before_merge']}
    return {'project_approvals_before_merge': 'ERROR'}

def check_project_push_rules_unsigned_commits(project):
    if project.project_push_rules is not None:
        return {'project_push_rules_unsigned_commits': project.project_push_rules.reject_unsigned_commits}
    return {'project_push_rules_unsigned_commits': 'ERROR'}

def check_project_push_rules_comitter_check(project):
    if project.project_push_rules is not None:
        return {'project_push_rules_comitter_check': project.project_push_rules.commit_committer_check}
    return {'project_push_rules_comitter_check': 'ERROR'}

def check_project_protected_branches(project):
    if project.project_protected_branches is not None:
        project_protected_branches_list = []
        for i in project.project_protected_branches:
            project_protected_branches = i
            try:
                project_protected_branches_list.append(project_protected_branches._attrs)
            except:
                project_protected_branches_list.append(project_protected_branches)
        return {'project_protected_branches': project_protected_branches_list}
    return {'project_protected_branches': 'ERROR'}

def check_project_access_tokens(project):
    if project.project_access_tokens is not None:
        project_access_tokens_list = []
        for i in project.project_access_tokens:
            project_access_tokens = i
            try:
                project_access_tokens_list.append(project_access_tokens._attrs)
            except:
                project_access_tokens_list.append(project_access_tokens)
        return {'project_access_tokens': project_access_tokens_list}
    return {'project_access_tokens': 'ERROR'}

def check_project_deploy_tokens(project):
    if project.project_deploy_tokens is not None:
        project_deploy_tokens_list = []
        for i in project.project_deploy_tokens:
            project_deploy_tokens = i
            try:
                project_deploy_tokens_list.append(project_deploy_tokens._attrs)
            except:
                project_deploy_tokens_list.append(project_deploy_tokens)
        return {'project_deploy_tokens': project_deploy_tokens_list}
    return {'project_deploy_tokens': 'ERROR'}

def check_project_deploy_keys(project):
    if project.project_deploy_keys is not None:
        project_deploy_keys_list = []
        for i in project.project_deploy_keys:
            project_deploy_keys = i
            try:
                project_deploy_keys_list.append(project_deploy_keys._attrs)
            except:
                project_deploy_keys_list.append(project_deploy_keys)
        return {'project_deploy_keys': project_deploy_keys_list}
    return {'project_deploy_keys': 'ERROR'}

def check_project_file_pipeline(project):
    if project.project_file_pipeline is not None:
        return {'project_file_pipeline': project.project_file_pipeline}
    return {'project_file_pipeline': 'ERROR'}

def check_project_merged_pipeline(project):
    if project.project_merged_pipeline is not None:
        return {'project_merged_pipeline': project.project_merged_pipeline}
    return {'project_merged_pipeline': 'ERROR'}

def check_project_merged_pipeline_stages(project):
    if project.project_merged_pipeline is not None:
        pipeline_block_stages = project.get_project_merged_pipeline_block(project.project_merged_pipeline, 'stages')
        return {'project_merged_pipeline_stages': pipeline_block_stages}
    return {'project_merged_pipeline_stages': 'ERROR'}

def check_project_merged_pipeline_images(project):
    if project.project_merged_pipeline is not None:
        pipeline_block_images = project.get_project_merged_pipeline_content_of_block(project.project_merged_pipeline, 'image')
        return {'project_merged_pipeline_image': pipeline_block_images}
    return {'project_merged_pipeline_image': 'ERROR'}

def check_project_file_codeowners(project):
    if project.project_file_codeowners is not None:
        return {'project_file_codeowners': project.project_file_codeowners}
    return {'project_file_codeowners': 'ERROR'}
    
def check_project_shared_runners_enabled(project):
    if project.project_shared_runers_enabled is not None:
        return {'project_shared_runners_enabled': project.project_shared_runers_enabled}
    return {'project_shared_runners_enabled': 'ERROR'}

def check_project_runners(project):
    if project.project_runners is not None:
        project_runners_list = []
        for i in project.project_runners:
            project_runners = i
            try:
                project_runners_list.append(project_runners._attrs)
            except:
                project_runners_list.append(project_runners)
        return {'project_runners': project_runners_list}
    return {'project_runners': 'ERROR'}

def check_project_runners_shared(project):
    if project.project_runners is not None:
        project_runners_list = []
        for i in project.project_runners:
            project_runners = i
            try:
                if project_runners._attrs['is_shared']:
                    project_runners_list.append(project_runners._attrs)
            except:
                project_runners_list.append(project_runners)
        return {'project_runners_shared': project_runners_list}
    return {'project_runners_shared': 'ERROR'}

def check_project_runners_notshared(project):
    if project.project_runners is not None:
        project_runners_list = []
        for i in project.project_runners:
            project_runners = i
            try:
                if not project_runners._attrs['is_shared']:
                    project_runners_list.append(project_runners._attrs)
            except:
                project_runners_list.append(project_runners)
        return {'project_runners_notshared': project_runners_list}
    return {'project_runners_notshared': 'ERROR'}

def check_project_log4j(project):
    if not project.project_search_log4j:
        return {'project_log4j': False}
    check_findings = []
    for findings in project.project_search_log4j:
        check_findings.append(findings['data'])
    return {'project_log4j': check_findings}