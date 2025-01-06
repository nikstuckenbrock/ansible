import tpm
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: teampasswordmanager_password_create
short_description: Create new passwords.
version_added: "0.1.0"
description: Create new passwords in the TeamPasswordManager.
options:
    url:
        type: str
        required: true
    private_key:
        type: str
        required: true
    public_key:
        type: str
        required: true
    name:
        type: str
        required: true
    project_id:
        type: int
        required: true
    tags:
        type: str
        required: false
    username:
        type: str
        required: false
    email:
        type: str
        required: false
    password:
        type: str
        required: false
    notes:
        type: str
        required: false
author:
    - Nik Stuckenbrock (@nikstuckenbrock)
'''

EXAMPLES = r'''
# Create a new password
- name: Test with a message
  nikstuckenbrock.teampasswordmanager.teampasswordmanager_password_create.py:
    url: https://example.com
    private_key: 0123456789
    public_key: 0123456789
'''

RETURNS = r'''
message:
    description: The output message if a password was created.
    type: str
    returned: always
    sample: 'created'
'''

fields: list[str] = [
    "name",
    "project_id",
    "tags",
    "username",
    "email",
    "password",
    "notes"
]

def run_module() -> None:
    module_args: dict = dict(
        url=dict(type='str', required=True),
        private_key=dict(type='str', required=True),
        public_key=dict(type='str', required=True),
        name=dict(type='str', required=True),
        project_id=dict(type='int', required=True),
        tags=dict(type='str', required=False),
        username=dict(type='str', required=False),
        email=dict(type='str', required=False),
        password=dict(type='str', required=False),
        notes=dict(type='str', required=False)
    )

    result: dict = dict(
        changed=False,
        original_message='',
        message=''
    )

    module: AnsibleModule = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    api: tpm.TpmApiv5 = tpm.TpmApiv5(
        url=module.params["url"],
        private_key=module.params["private_key"],
        public_key=module.params["public_key"],
    )

    data: dict = {}
    for argument in module_args.keys():
        if argument in fields:
            data[argument] = module.params[argument]
            
    api.create_password(
        data=data
    )
    
    result['message'] = 'created'
    
def main():
    run_module()

if __name__ == "__main__":
    main()
