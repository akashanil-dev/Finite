"""Local-only role management; never grants admin based on registration order or a reserved name."""
import argparse
from . import db


def set_admin(username, enabled):
    db.init()
    with db.tx() as c:
        result = c.execute('UPDATE users SET is_admin=? WHERE username=?', (int(enabled), username.strip().lower()))
        if not result.rowcount:
            raise ValueError('Account not found; register and verify the account first')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('username')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--admin', action='store_true')
    group.add_argument('--revoke-admin', action='store_true')
    args = parser.parse_args()
    try:
        set_admin(args.username, args.admin)
        print('Account role updated')
    except ValueError as exc:
        parser.exit(1, str(exc) + '\n')
