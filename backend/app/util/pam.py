import pam
import secrets

_pam = pam.pam()


def authenticate_user(username: str, password: str) -> bool:
    return _pam.authenticate(username, password)

def is_superuser(username: str) -> bool:
    try:
        user = pwd.getpwnam(username)
        
        if user.pw_uid == 0:
            return True

        groups = os.getgrouplist(
            username,
            user.pw_gid
        )

        sudo_group = grp.getgrnam("sudo")

        return sudo_group.gr_gid in groups

    except KeyError:
        return False