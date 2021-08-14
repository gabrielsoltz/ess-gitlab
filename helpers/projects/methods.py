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

def get_all_projects(gl):
    #projects = gl.projects.list(all=True)
    projects = gl.groups.list(page=1, per_page=10)
    return projects