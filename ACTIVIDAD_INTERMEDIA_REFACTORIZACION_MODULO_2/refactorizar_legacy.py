def process(u, pw, r, db):
    import hashlib
    h = hashlib.md5(pw.encode()).hexdigest()
    for x in db:
        if x[0] == u and x[1] == h:
            if r == 'admin':
                return {'ok': True, 'lvl': 3, 'msg': 'Admin OK'}
            elif r == 'user':
                return {'ok': True, 'lvl': 1, 'msg': 'User OK'}
            else:
                return {'ok': True, 'lvl': 0, 'msg': 'Guest OK'}
    return {'ok': False, 'lvl': -1, 'msg': 'Auth failed'}