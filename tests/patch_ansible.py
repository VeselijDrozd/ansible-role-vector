# patch_ansible.py
# simple helper to add missing symbol in ansible.galaxy.api for 3.x
import ansible.galaxy.api as api
if not hasattr(api, "should_retry_error"):
    def should_retry_error(*args, **kwargs):
        return False
    api.should_retry_error = should_retry_error
