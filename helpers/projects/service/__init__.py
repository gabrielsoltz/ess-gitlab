import yaml

def get_protectedbranches(gl, project_id):
    project = gl.projects.get(project_id)
    return project.protectedbranches.list()
    
def get_project_attributes(gl, project_id):
    project = gl.projects.get(project_id)
    return project.attributes

def get_project_access_tokens(gl, project_id):
    project = gl.projects.get(project_id)
    return project.access_tokens.list()

def get_project_deployment_tokens(gl, project_id):
    project = gl.projects.get(project_id)
    return project.deploytokens.list()

def get_project_keys(gl, project_id):
    project = gl.projects.get(project_id)
    return project.keys.list()

def get_project_push_rules(gl, project_id):
    project = gl.projects.get(project_id)
    return project.pushrules.get()

def get_project_languages(gl, project_id):
    project = gl.projects.get(project_id)
    return project.languages()

def get_project_contributors(gl, project_id):
    project = gl.projects.get(project_id)
    return project.repository_contributors()

def get_project_ids(gl, id):

    project_ids_list = []

    if id == 'all':
        type = 'all'
        #projects = gl.projects.list(all=True)
        projects = gl.groups.list(page=1, per_page=10, lazy=True)
        for project in projects:
            project_ids_list.append(project.id)
        return project_ids_list, type

    try:
        group = gl.groups.get(id, lazy=True)
        projects = group.projects.list(include_subgroups=True, all=True, lazy=True)
    #except gitlab.exceptions.GitlabListError:
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

def get_project_file(gl, project_id, file):
    project = gl.projects.get(project_id)
    f = project.files.raw(file_path=file, ref='master')
    return f.decode()

def get_project_pipeline_block(pipeline_file, block):
    try: 
        pipeline_block = yaml.safe_load(pipeline_file)[block]
        return {'project_pipeline_' + block: pipeline_block}
    except KeyError:
        return {'project_pipeline_' + block: 'Block Not Found'}
    except:
        return {'project_pipeline_' + block: 'Error'}

def get_project_pipeline_content_of_block(pipeline_file, block):
    project_pipeline_images = {'project_pipeline_' + block: []}
    try:
        pipeline_yaml = yaml.safe_load(pipeline_file)
    except:
        return project_pipeline_images
    for i in pipeline_yaml:
        if str(i).strip().lower() == block:
            project_pipeline_images['project_pipeline_' + block].append(pipeline_yaml[i])
        if str(pipeline_yaml[i]).strip().lower() == block:
            project_pipeline_images['project_pipeline_' + block].append(pipeline_yaml[i][block])
        for j in pipeline_yaml[i]:
             if str(j).strip().lower() == block:     
                project_pipeline_images['project_pipeline_' + block].append(pipeline_yaml[i][block])
    return project_pipeline_images