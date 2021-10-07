# EasyScan Gitlab

! THIS IS A WORK IN PROGRESS

Easy Scanning for Gitlab Mis-Configurations

This tool can run in 2 different modes (`--mode`):

- Inventory: It will fetch all the information for a specific scope (`check` + `id`).
- Baseline: It will fetch all the information for a specific scope (`check` + `id`) and compare with the baseline definition for that scope for generating a miss-configuration report

## How to use it

You can define `--id` as a "project id", as a "group id" for getting all project ids under that group or "all" for getting all project ids.

### Inventory Mode

`./easyscan-gitlab.py  --gitlab_url https://yourgitlab.com --gitlab_token yourgitlabtoken --mode inventory --check project --id <PROJECT_ID>/<GROUP ID>/all`

### Baseline Mode

`./easyscan-gitlab.py  --gitlab_url https://yourgitlab.com --gitlab_token yourgitlabtoken --mode baseline --check project --id <PROJECT_ID>/<GROUP ID>/all`

## Baselines Use Cases

### Check if "Push Rules: Unsigned Commits" and "Push Rules: Comitter Check" are enabled for all projects (`*`)

Baseline:
```
projects:
  - '*':
    - project_visibility:
    - project_pages_access_level:
    - project_security_and_compliance_enabled:
    - project_approvals_before_merge: 
    - project_push_rules_unsigned_commits: true
    - project_push_rules_comitter_check: true
    - project_protected_branches: 
    - project_access_tokens:
    - project_deployment_tokens:
    - project_keys:
    - project_pipeline: 
    - project_pipeline_stages: []
    - project_pipeline_image: []
    - project_codeowners: 
```

### Check if "Project Visibility" is `internal` for project `1234` and `public` for project `4321`

Baseline:
```
projects:
  - '1234':
    - project_visibility: internal
    - project_pages_access_level:
    - project_security_and_compliance_enabled:
    - project_approvals_before_merge: 
    - project_push_rules_unsigned_commits: true
    - project_push_rules_comitter_check: true
    - project_protected_branches: 
    - project_access_tokens:
    - project_deployment_tokens:
    - project_keys:
    - project_pipeline: 
    - project_pipeline_stages: []
    - project_pipeline_image: []
    - project_codeowners: 
  - '4321':
    - project_visibility: public
    - project_pages_access_level:
    - project_security_and_compliance_enabled:
    - project_approvals_before_merge: 
    - project_push_rules_unsigned_commits: true
    - project_push_rules_comitter_check: true
    - project_protected_branches: 
    - project_access_tokens:
    - project_deployment_tokens:
    - project_keys:
    - project_pipeline: 
    - project_pipeline_stages: []
    - project_pipeline_image: []
    - project_codeowners: 
```

### Check if any project is using the image `docker:latest` in any stage of the pipeline:

Baseline:
```
projects:
  - '*':
    - project_visibility:
    - project_pages_access_level:
    - project_security_and_compliance_enabled:
    - project_approvals_before_merge: 
    - project_push_rules_unsigned_commits:
    - project_push_rules_comitter_check:
    - project_protected_branches: 
    - project_access_tokens:
    - project_deployment_tokens:
    - project_keys:
    - project_pipeline: 
    - project_pipeline_stages: []
    - project_pipeline_image: ['docker:latest']
    - project_codeowners: 
```

### Check if any project is using `project_keys`, `project_deployment_tokens`, or `project_access_tokens`:

Baseline:
```
projects:
  - '*':
    - project_visibility:
    - project_pages_access_level:
    - project_security_and_compliance_enabled:
    - project_approvals_before_merge: 
    - project_push_rules_unsigned_commits:
    - project_push_rules_comitter_check:
    - project_protected_branches: 
    - project_access_tokens: ''
    - project_deployment_tokens: ''
    - project_keys: ''
    - project_pipeline: 
    - project_pipeline_stages: []
    - project_pipeline_image: []
    - project_codeowners: 
```

## Checks: Project

- Project Visibility
- Pages Access Level
- Security and Compliance
- Approvals before Merge
- Push Rules: Unsigned Commits
- Push Rules: Comitter Check
- Protected Branches
- Project Access Tokens
- Project Deployment Tokens
- Project Keys
- Project Pipeline: file
- Project Pipeline: check Blocks
- Project Pipeline: check Images in all blocks
- Project CODEOWNERS file


### Project Visibility

These visibility levels affect who can see the project in the public access directory (/public for your GitLab instance). For example, https://gitlab.com/public. You can control the visibility of individual features with project feature settings.

https://docs.gitlab.com/ee/public_access/public_access.html


### Pages Access Level

https://docs.gitlab.com/ee/user/project/pages/pages_access_control.html

### Security and Compliance

https://docs.gitlab.com/ee/user/application_security/configuration/

### Approvals before Merge

https://docs.gitlab.com/ee/user/project/merge_requests/approvals/

### Push Rules: Unsigned Commits

https://docs.gitlab.com/ee/push_rules/push_rules.html

### Push Rules: Comitter Check

https://docs.gitlab.com/ee/push_rules/push_rules.html

### Protected Branches

https://docs.gitlab.com/ee/user/project/protected_branches.html

### Project Access Tokens

https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html

### Project Deployment Tokens

https://docs.gitlab.com/ee/user/project/deploy_tokens/

### Project Keys

https://docs.gitlab.com/ee/user/project/deploy_keys/

### Project Pipeline file

Check if file `.gitlab-ci.yml` exists.

#### Project Pipeline check Blocks (`stages`)

Show all stages from the pipeline

#### Project Pipeline check Images in all blocks (`image`)

Show all images being used in all stages of the pipeline

### Project CODEOWNERS file

Check if file CODEOWNERS exists.