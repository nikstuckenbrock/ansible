import tpm
from ansible.module_utils.basic import AnsibleModule

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
    
def main():
    run_module()

if __name__ == "__main__":
    main()
