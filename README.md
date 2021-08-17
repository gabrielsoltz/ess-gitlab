# EasyScan Gitlab

Easy Scanning for Gitlab Miss-Configurations

## How to use it

## Scan a specific project

`./easyscan-gitlab.py --gitlab_url https://yourgitlab.com --gitlab_token yourgitlabtoken --check project --project_id project_id_number`

## Scan all projects (hardcoded amount of projects: 10)

`./easyscan-gitlab.py --gitlab_url https://yourgitlab.com --gitlab_token yourgitlabtoken --check project --project_id all`

## Project Checks

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

### Project Keys

#### Project Access Tokens

https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html

#### Project Deployment Tokens

https://docs.gitlab.com/ee/user/project/deploy_tokens/

#### Project Keys

https://docs.gitlab.com/ee/user/project/deploy_keys/