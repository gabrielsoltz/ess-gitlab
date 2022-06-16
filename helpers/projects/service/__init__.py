import yaml
from gitlab import exceptions, SEARCH_SCOPE_BLOBS, Gitlab

class GitlabGroupService():
    
    def __init__(self, gl, id, logging, max_all):
        self.logging = logging
        self.group_id = id 
        get_project_ids = self.get_project_ids(gl, id, max_all)
        if get_project_ids:
            self.projects_ids = get_project_ids[0]
            self.group_type = get_project_ids[1]
            self.projects_len = len(self.projects_ids)
        else:
            self.projects_ids = ''
            self.group_type = 'ERROR'
            self.projects_len = 0

    def get_project_ids(self, gl, id, max_all):

        project_ids_list = []

        if id == 'all':
            type = 'all'
            print('Fetching all projects!')
            all_projects = gl.projects.list(as_list=False, lazy=True)
            all_project_len = len(all_projects)
            counter = 0
            for project in all_projects:
                counter += 1
                print('Projects fetched:', counter, '(total:', all_project_len, ')', end='\r')
                project_ids_list.append(project.id)
                if counter >= max_all:
                    break
            return project_ids_list, type

        try:
            group = gl.groups.get(id, lazy=True)
            projects = group.projects.list(include_subgroups=True, all=True, lazy=True)
        except:
            group = None
        if group:
            type = 'group'
            for project in projects:
                project_ids_list.append(project.id)
            return project_ids_list, type

        try:
            project = gl.projects.get(id)
        except:
            project = None
        if project:
            type = 'project'
            project_ids_list.append(id)
            return project_ids_list, type
        
        if project is None and group is None:
            self.logging.error('Error Wrong ID: {}'.format(id))
            return False

class GitlabProjectService():

    def __init__(self, gl, id, logging):
        self.gitlab_connection: Gitlab = gl
        self.logging = logging
        self.project_id = id 
        self.project = gl.projects.get(id)
        self.project_archived = self.get_project_archived()
        self.project_attributes = self.get_project_attributes()
        self.project_languages = self.get_project_languages()
        self.project_contributors = self.get_project_contributors()
        self.project_labels = self.get_project_labels()
        self.project_topics = self.get_project_topics()
        self.project_info = self.get_project_info()
        self.project_push_rules = self.get_project_push_rules()
        self.project_protected_branches = self.get_protectedbranches()
        self.project_access_tokens = self.get_project_access_tokens()
        self.project_deploy_tokens = self.get_project_deploy_tokens()
        self.project_deploy_keys = self.get_project_deploy_keys()
        self.project_file_pipeline = self.get_project_file('.gitlab-ci.yml')
        self.project_merged_pipeline = self.get_merged_pipeline()
        self.project_file_codeowners = self.get_project_file('CODEOWNERS')
        self.project_runners = self.get_project_runners()
        self.project_shared_runers_enabled = self.get_project_shared_runners_enabled()
        self.project_search_log4j = self.search_project('log4j')

    def get_project_info(self):
        project_info = {}
        if self.project_attributes is not None:
            project_info.update({'name': self.project_attributes['name'], 'name_with_namespace': self.project_attributes['name_with_namespace'], 'description': self.project_attributes['description'], 'web_url': self.project_attributes['web_url']})
        if self.project_languages is not None:
            project_info.update({'project_languages': self.project_languages})
        if self.project_contributors is not None:
            project_info.update({'project_contributors': self.project_contributors})
        if self.project_labels is not None:
            project_info.update({'project_labels': self.project_labels})
        if self.project_topics is not None:
            project_info.update({'project_topics': self.project_topics})
        return {'project_info': project_info}

    def get_project_labels(self):
        project_labels_list = []
        try:
            labels = self.project.labels.list()
            for i in labels:
                project_label = i
                try:
                    project_labels_list.append(project_label._attrs)
                except:
                    project_labels_list.append(project_label)
        except exceptions.GitlabGetError as e:
            self.logging.error('Error getting project {} labels: {}'.format(self.project_id, e))
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} labels: {}'.format(self.project_id, e))
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} labels: {}'.format(self.project_id, e))
        return project_labels_list

    def get_project_topics(self):
        topics = []
        try:
            topics = self.project.tag_list
        except exceptions.GitlabGetError as e:
            self.logging.error('Error getting project {} topics: {}'.format(self.project_id, e))
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} topics: {}'.format(self.project_id, e))
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} topics: {}'.format(self.project_id, e))
        return topics

    def get_project_archived(self):
        try:
            archived = self.project.archived
        except exceptions.GitlabGetError as e:
            self.logging.error('Error getting project {} archived: {}'.format(self.project_id, e))
            archived = None
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} archived: {}'.format(self.project_id, e))
            archived = None
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} archived: {}'.format(self.project_id, e))
            archived = None
        return archived

    def get_project_attributes(self):
        try:
            project_attributes = self.project.attributes
        except exceptions.GitlabGetError as e:
            self.logging.error('Error getting project {} attributes: {}'.format(self.project_id, e))
            project_attributes = None
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} attributes: {}'.format(self.project_id, e))
            project_attributes = None
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} attributes: {}'.format(self.project_id, e))
            project_attributes = None
        return project_attributes

    def get_project_languages(self):
        try:
            project_languages = self.project.languages()
        except exceptions.GitlabGetError as e:
            self.logging.error('Error getting project {} languages: {}'.format(self.project_id, e))
            project_languages = None
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} languages: {}'.format(self.project_id, e))
            project_languages = None
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} languages: {}'.format(self.project_id, e))
            project_languages = None
        return project_languages

    def get_project_contributors(self):
        try:
            project_contributors = self.project.repository_contributors()
        except exceptions.GitlabGetError as e:
            self.logging.error('Error getting project {} contributors: {}'.format(self.project_id, e))
            project_contributors = None
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} contributors: {}'.format(self.project_id, e))
            project_contributors = None
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} contributors: {}'.format(self.project_id, e))
            project_contributors = None
        return project_contributors

    def get_project_push_rules(self):
        try:
            push_rules = self.project.pushrules.get()
        except exceptions.GitlabGetError as e:
            self.logging.error('Error getting project {} push rules: {}'.format(self.project_id, e))
            push_rules = None
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} push rules: {}'.format(self.project_id, e))
            push_rules = None
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} push rules: {}'.format(self.project_id, e))
            push_rules = None
        return push_rules

    def get_protectedbranches(self):
        try:
            protectedbranches = self.project.protectedbranches.list()
        except exceptions.GitlabGetError as e:
            self.logging.error('Error getting project {} protected branches: {}'.format(self.project_id, e))
            protectedbranches = None
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} protected branches: {}'.format(self.project_id, e))
            protectedbranches = None
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} protected branches: {}'.format(self.project_id, e))
            protectedbranches = None
        return protectedbranches
        
    def get_project_access_tokens(self):
        try:
            access_tokens = self.project.access_tokens.list()
        except exceptions.GitlabGetError as e:
            self.logging.error('Error getting project {} access tokens: {}'.format(self.project_id, e))
            access_tokens = None
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} access tokens: {}'.format(self.project_id, e))
            access_tokens = None
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} access tokens: {}'.format(self.project_id, e))
            access_tokens = None
        return access_tokens

    def get_project_deploy_tokens(self):
        try:
            deploy_tokens = self.project.deploytokens.list()
        except exceptions.GitlabGetError as e:
            self.logging.error('Error getting project {} deploy tokens: {}'.format(self.project_id, e))
            deploy_tokens = None
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} deploy tokens: {}'.format(self.project_id, e))
            deploy_tokens = None
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} deploy tokens: {}'.format(self.project_id, e))
            deploy_tokens = None
        return deploy_tokens

    def get_project_deploy_keys(self):
        try:
            deploy_keys = self.project.keys.list()
        except exceptions.GitlabGetError as e:
            self.logging.error('Error getting project {} deploy keys: {}'.format(self.project_id, e))
            deploy_keys = None
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} deploy keys: {}'.format(self.project_id, e))
            deploy_keys = None
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} deploy keys: {}'.format(self.project_id, e))
            deploy_keys = None
        return deploy_keys

    def get_project_file(self, file):
        try:
            project_file = self.project.files.raw(file_path=file, ref='master')
            return project_file.decode()
        except exceptions.GitlabGetError as e:
            if '404' in str(e):
                project_file = False
            else:
                self.logging.error('Error getting project {} file: {} {}'.format(self.project_id, file, e))
                project_file = None
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} file: {} {}'.format(self.project_id, file, e))
            project_file = None
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} file: {} {}'.format(self.project_id, file, e))
            project_file = None
        return project_file

    def get_merged_pipeline(self):
        try:
            response = self.gitlab_connection.http_get(f"/projects/{self.project_id}/ci/lint")
            try:
                pipeline = yaml.safe_load(response["merged_yaml"])
            except AttributeError as e:
                errors = response["errors"]
                self.logging.error('Error getting project {} merged pipeline: {} - {}'.format(self.project_id, e, errors))
                pipeline = False
        except exceptions.GitlabError as e:
            self.logging.error('Error getting project {} merged pipeline: {}'.format(self.project_id, e))
            pipeline = None
        return pipeline

    def get_project_merged_pipeline_block(self, pipeline_yaml, block):
        if self.project_merged_pipeline:
            try: 
                pipeline_block = pipeline_yaml[block]
            except KeyError:
                pipeline_block = False
            except:
                self.logging.error('Error getting project {} pipeline block: {}'.format(self.project_id, block))
                pipeline_block = None
        else:
            pipeline_block = []
        return pipeline_block

    def get_project_merged_pipeline_content_of_block(self, pipeline_yaml, block):
        pipeline_block_content = []
        if self.project_merged_pipeline:
            for i in pipeline_yaml:
                if str(i).strip().lower() == block:
                    pipeline_block_content.append(pipeline_yaml[i])
                if str(pipeline_yaml[i]).strip().lower() == block:
                    pipeline_block_content.append(pipeline_yaml[i][block])
                for j in pipeline_yaml[i]:
                    if str(j).strip().lower() == block:
                        pipeline_block_content.append(pipeline_yaml[i][j])
        return pipeline_block_content

    def get_project_shared_runners_enabled(self):
        return self.project.shared_runners_enabled
    
    def get_project_runners(self):
        try:
            runners = self.project.runners.list()
        except exceptions.GitlabGetError as e:
            self.logging.error('Error getting project {} runners: {}'.format(self.project_id, e))
            runners = None
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error getting project {} runners: {}'.format(self.project_id, e))
            runners = None
        except exceptions.GitlabListError as e:
            self.logging.error('Error getting project {} runners: {}'.format(self.project_id, e))
            runners = None
        return runners
    
    def search_project(self, string_to_search):
        try:
            project_search = self.project.search(SEARCH_SCOPE_BLOBS, string_to_search)
        except exceptions.GitlabGetError as e:
            self.logging.error('Error searching project {}: {}'.format(self.project_id, e))
            project_search = None
        except exceptions.GitlabAuthenticationError as e:
            self.logging.error('Error searching project {}: {}'.format(self.project_id, e))
            project_search = None
        except exceptions.GitlabListError as e:
            self.logging.error('Error searching project {}: {}'.format(self.project_id, e))
            project_search = None
        return project_search