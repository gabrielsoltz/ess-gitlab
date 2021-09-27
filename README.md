# EasyScan Gitlab

! THIS IS A WORK IN PROGRESS

Easy Scanning for Gitlab Mis-Configurations

This tool can run in 2 different modes (`--mode`):

- Inventory: It will fetch all the information for a specific scope (`check` + `id`).
- Baseline: It will fetch all the information for a specific scope (`check` + `id`) and compare with the baseline definition for that scope for generating a miss-configuration report

## How to use it

### Inventory Mode

You can define `--id` as a project id, a group id for getting all project ids under that group or all for getting all project ids.

`./easyscan-gitlab.py  --gitlab_url https://yourgitlab.com --gitlab_token yourgitlabtoken --mode inventory --check project --id <PROJECT_ID>/<GROUP ID>/all`

### Baseline for a specific project

`./easyscan-gitlab.py  --gitlab_url https://yourgitlab.com --gitlab_token yourgitlabtoken --mode baseline --check project --id <PROJECT_ID>/<GROUP ID>/all`

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