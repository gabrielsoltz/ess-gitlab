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

### Optional Arguments

- `--jsonfile`: Generates JSON file with output (inventory or baseline). Default: True
- `--baseline`: Defines where is the baseline file. Default: `baselines/default.yml`
- `--log`: Logger level. Valid Options: ERROR, INFO or DEBUG. Default: ERROR

## Baselines

You can define a baseline using the following type of values:

- None: Check disabled
- String: Matching string to output (Example: 'internal')
- Bool: True matchs if output has data or if output True. False matchs if no Data or if output False.
- List: At least 1 of the values must be in the output (Example: '[docker:latest]'). Empty list ('[]') same as False.

You can define values for all projects using '*' or for a specific project using the project id like '1234'. You can add more than one project id in each baseline.

TO DO: Baselines by Group IDs. 

### Check if "Push Rules: Unsigned Commits" and "Push Rules: Comitter Check" are enabled for all projects (`*`)

Baseline:
```
projects:
  - '*':
    - project_visibility: None
    - project_pages_access_level: None
    - project_security_and_compliance_enabled: None
    - project_approvals_before_merge: None
    - project_push_rules_unsigned_commits: True
    - project_push_rules_comitter_check: True
    - project_protected_branches: None
    - project_access_tokens: None
    - project_deploy_tokens: None
    - project_deploy_keys: None
    - project_pipeline: None
    - project_pipeline_stages: None
    - project_pipeline_image: None
    - project_codeowners: None
```

### Check if "Project Visibility" is `internal` for project `1234` and `public` for project `4321`

Baseline:
```
projects:
  - '1234':
    - project_visibility: internal
    - project_pages_access_level: None
    - project_security_and_compliance_enabled: None
    - project_approvals_before_merge:  None
    - project_push_rules_unsigned_commits: None
    - project_push_rules_comitter_check: None
    - project_protected_branches: None
    - project_access_tokens: None
    - project_deploy_tokens: None
    - project_deploy_keys: None
    - project_pipeline: None
    - project_pipeline_stages: None
    - project_pipeline_image: None
    - project_codeowners: None
  - '4321':
    - project_visibility: public
    - project_pages_access_level: None
    - project_security_and_compliance_enabled: None
    - project_approvals_before_merge:  None
    - project_push_rules_unsigned_commits: None
    - project_push_rules_comitter_check: None
    - project_protected_branches: None
    - project_access_tokens: None
    - project_deploy_tokens: None
    - project_deploy_keys: None
    - project_pipeline: None
    - project_pipeline_stages: None
    - project_pipeline_image: None
    - project_codeowners: None
```

### Check if any project is using the image `docker:latest` in any stage of the pipeline:

Baseline:
```
projects:
  - '*':
    - project_visibility: None
    - project_pages_access_level: None
    - project_security_and_compliance_enabled: None
    - project_approvals_before_merge:  None
    - project_push_rules_unsigned_commits: None
    - project_push_rules_comitter_check: None
    - project_protected_branches: None
    - project_access_tokens: None
    - project_deploy_tokens: None
    - project_deploy_keys: None
    - project_pipeline: None
    - project_pipeline_stages: None
    - project_pipeline_image: ['docker:latest']
    - project_codeowners: None
```

### Check if `project_deploy_keys`, `project_deploy_tokens`, or `project_access_tokens` are not being used:

Baseline:
```
projects:
  - '*':
    - project_visibility: None
    - project_pages_access_level: None
    - project_security_and_compliance_enabled: None
    - project_approvals_before_merge:  None
    - project_push_rules_unsigned_commits: None
    - project_push_rules_comitter_check: None
    - project_protected_branches: None
    - project_access_tokens: False
    - project_deploy_tokens: False
    - project_deploy_keys: False
    - project_pipeline: None
    - project_pipeline_stages: None
    - project_pipeline_image: None
    - project_codeowners: None
```

### Check if Pipeline file (`.gitlab-ci.yml`) exists:

Baseline:
```
projects:
  - '*':
    - project_visibility: None
    - project_pages_access_level: None
    - project_security_and_compliance_enabled: None
    - project_approvals_before_merge:  None
    - project_push_rules_unsigned_commits: None
    - project_push_rules_comitter_check: None
    - project_protected_branches: None
    - project_access_tokens: None
    - project_deploy_tokens: None
    - project_deploy_keys: None
    - project_pipeline: True
    - project_pipeline_stages: None
    - project_pipeline_image: None
    - project_codeowners: None
```

### Check if CODEOWNERS file (`CODEOWNERS`) exists:

Baseline:
```
projects:
  - '*':
    - project_visibility: None
    - project_pages_access_level: None
    - project_security_and_compliance_enabled: None
    - project_approvals_before_merge:  None
    - project_push_rules_unsigned_commits: None
    - project_push_rules_comitter_check: None
    - project_protected_branches: None
    - project_access_tokens: None
    - project_deploy_tokens: None
    - project_deploy_keys: None
    - project_pipeline: None
    - project_pipeline_stages: None
    - project_pipeline_image: None
    - project_codeowners: True
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
- Project Deploy Tokens
- Project Deploy Keys
- Project Pipeline: file
- Project Pipeline block: `stages`
- Project Pipeline block: `image`
- Project CODEOWNERS file


### Project Visibility

- [Gitlab Documentation](https://docs.gitlab.com/ee/public_access/public_access.html)
- Baseline Key: `project_visibility`
- Inventory Outputs: `internal`, `public`, `private`
- Default Baseline: `internal`

### Pages Access Level

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/pages/pages_access_control.html)
- Baseline Key: `project_pages_access_level`
- Inventory Outputs: `public`,
- Default Baseline:

### Security and Compliance

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/application_security/configuration/)
- Baseline Key: `project_security_and_compliance_enabled`
- Inventory Outputs: `true`, `false`
- Default Baseline: `true`

### Approvals before Merge

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- Baseline Key: `project_approvals_before_merge`
- Inventory Outputs: Number of Approvals before Merge
- Default Baseline: `1`
- TO DO: optional/required different output

### Push Rules: Unsigned Commits

- [Gitlab Documentation](https://docs.gitlab.com/ee/push_rules/push_rules.html)
- Baseline Key: `project_push_rules_unsigned_commits`
- Inventory Outputs: `true`, `false`
- Default Baseline: `true`

### Push Rules: Comitter Check

- [Gitlab Documentation](https://docs.gitlab.com/ee/push_rules/push_rules.html)
- Baseline Key: `project_push_rules_comitter_check`
- Inventory Outputs: `true`, `false`
- Default Baseline: `true`

### Protected Branches

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/protected_branches.html)
- Baseline Key: `project_protected_branches`
- Inventory Outputs: List of Protected Branches
- Default Baseline: `true`
- TO DO: Check by branch

### Project Access Tokens

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html)
- Baseline Key: `project_access_tokens`
- Inventory Outputs: List of Project Access Tokens
- Default Baseline: `false`

### Project Deploy Tokens

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/deploy_tokens/)
- Baseline Key: `project_deploy_tokens`
- Inventory Outputs: List of Project Deploy Tokens
- Default Baseline: `false`

### Project Deploy Keys

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/deploy_keys/)
- Baseline Key: `project_deploy_keys`
- Inventory Outputs: List of Project Deploy Keys
- Default Baseline: `false`

### Project Pipeline file

- [Gitlab Documentation](https://docs.gitlab.com/ee/ci/pipelines/index.html)
- Baseline Key: `project_pipeline`
- Inventory Outputs: `true`, `false`
- Default Baseline: `true`

#### Project Pipeline block: `stages`

- [Gitlab Documentation](https://docs.gitlab.com/ee/ci/pipelines/pipeline_architectures.html)
- Baseline Key: `project_pipeline_stages`
- Posible Outputs: List with all pipeline Stages
- Default Baseline: `None`

#### Project Pipeline block: `image`

- [Gitlab Documentation](https://docs.gitlab.com/ee/ci/pipelines/pipeline_architectures.html)
- Baseline Key: `project_pipeline_image`
- Posible Outputs: List with all images in any stage of the pipeline
- Default Baseline: `None`

### Project CODEOWNERS file

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/code_owners.html)
- Baseline Key: `project_codeowners`
- Inventory Outputs: `true`, `false`
- Default Baseline: `True`