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

### Check if Pipeline file (`.gitlab-ci.yml`) exists:

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
    - project_pipeline: true
    - project_pipeline_stages: []
    - project_pipeline_image: []
    - project_codeowners: 
```

### Check if CODEOWNERS file (`CODEOWNERS`) exists:

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
    - project_pipeline_image: []
    - project_codeowners: true
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

- [Gitlab Documentation](https://docs.gitlab.com/ee/public_access/public_access.html)
- Baseline Key: `project_visibility`
- Posible Outputs: `internal`, `public`, `private`
- Default Baseline: `internal`

### Pages Access Level

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/pages/pages_access_control.html)
- Baseline Key: `project_pages_access_level`
- Posible Outputs:
- Default Baseline:

### Security and Compliance

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/application_security/configuration/)
- Baseline Key: `project_security_and_compliance_enabled`
- Posible Outputs: `boolean` (`true`/`false`)
- Default Baseline: `true`

### Approvals before Merge

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- Baseline Key: `project_approvals_before_merge`
- Posible Outputs: `integer`
- Default Baseline: `1`
- TO DO: optional/required different output

### Push Rules: Unsigned Commits

- [Gitlab Documentation](https://docs.gitlab.com/ee/push_rules/push_rules.html)
- Baseline Key: `project_push_rules_unsigned_commits`
- Posible Outputs: `boolean` (`true`/`false`)
- Default Baseline: `true`

### Push Rules: Comitter Check

- [Gitlab Documentation](https://docs.gitlab.com/ee/push_rules/push_rules.html)
- Baseline Key: `project_push_rules_comitter_check`
- Posible Outputs: `boolean` (`true`/`false`)
- Default Baseline: `true`

### Protected Branches

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/protected_branches.html)
- Baseline Key: `project_protected_branches`
- Posible Outputs: `boolean` (`true`/`false`)
- Default Baseline: `true`
- TO DO: Check by branch

### Project Access Tokens

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html)
- Baseline Key: `project_access_tokens`
- Posible Outputs: `boolean` (`true`/`false`)
- Default Baseline: `false`

### Project Deployment Tokens

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/deploy_tokens/)
- Baseline Key: `project_deploy_tokens`
- Posible Outputs: `boolean` (`true`/`false`)
- Default Baseline: `false`

### Project Keys

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/deploy_keys/)
- Baseline Key: `project_deploy_tokens`
- Posible Outputs: `boolean` (`true`/`false`)
- Default Baseline: `false`

### Project Pipeline file

- [Gitlab Documentation](https://docs.gitlab.com/ee/ci/pipelines/index.html)
- Baseline Key: `project_pipeline`
- Posible Outputs: `boolean` (`true`/`false`)
- Default Baseline: `true`

#### Project Pipeline check Blocks (`stages`)

- [Gitlab Documentation](https://docs.gitlab.com/ee/ci/pipelines/pipeline_architectures.html)
- Baseline Key: `project_pipeline_stages`
- Posible Outputs: `list with all stages`
- Default Baseline:

#### Project Pipeline check Images in all blocks (`image`)

- [Gitlab Documentation](https://docs.gitlab.com/ee/ci/pipelines/pipeline_architectures.html)
- Baseline Key: `project_pipeline_image`
- Posible Outputs: `list with all images`
- Default Baseline:

### Project CODEOWNERS file

- [Gitlab Documentation](https://docs.gitlab.com/ee/user/project/code_owners.html)
- Baseline Key: `project_codeowners`
- Posible Outputs: `boolean` (`true`/`false`)
- Default Baseline: `true`