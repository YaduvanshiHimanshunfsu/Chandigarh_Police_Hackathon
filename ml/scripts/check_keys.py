import lmdb

train_path = r"A:\DocTamper Dataset\DocTamperV1-TrainingSet"
fcd_path   = r"A:\DocTamper Dataset\DocTamperV1-FCD"
scd_path   = r"A:\DocTamper Dataset\DocTamperV1-SCD"

# Get first 5 keys from each
for name, path in [("TrainingSet", train_path), 
                    ("FCD", fcd_path), 
                    ("SCD", scd_path)]:
    env = lmdb.open(path, readonly=True, lock=False)
    with env.begin() as txn:
        total = txn.stat()['entries']
        cursor = txn.cursor()
        keys = []
        for i, (key, _) in enumerate(cursor):
            keys.append(key.decode('utf-8'))
            if i >= 4:
                break
    env.close()
    print(f"\n{name} ({total} total):")
    for k in keys:
        print(f"  {k}")