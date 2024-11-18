from sqlalchemy import select

from database import BlacklistTokens, db

def tokenNotBlacklist(token):
    stmt = select(BlacklistTokens).where(BlacklistTokens.token == token)
    rows = db.session.execute(stmt).one_or_none()
    if rows is not None:
        return False
    return True