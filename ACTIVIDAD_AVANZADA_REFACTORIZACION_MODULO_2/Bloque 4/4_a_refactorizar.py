def do_stuff(ords, disc, inv):
    res = []
    for o in ords:
        t = 0
        for item in o['items']:
            found = False
            for i in inv:
                if i['id'] == item['id']:
                    if i['stock'] > 0:
                        t += item['qty'] * i['price']
                        found = True
                        break
            if not found:
                print('Item not found: ' + str(item['id']))
        if o['type'] == 'premium':
            t = t * (1 - disc['premium'])
        elif o['type'] == 'vip':
            t = t * (1 - disc['vip'])
            if t > 1000:
                t = t * 0.95
        elif o['type'] == 'bulk':
            if len(o['items']) > 10:
                t = t * (1 - disc['bulk'])
        res.append({'order_id': o['id'], 'total': round(t, 2)})
    return res