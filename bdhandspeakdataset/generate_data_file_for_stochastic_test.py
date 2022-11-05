import pickle

import gzip

def load_dataset_file(filename):
    with gzip.open(filename, "rb") as f:
        loaded_object = pickle.load(f)
        return loaded_object

samples = {}

path = './data_for_stochastic/phoenix14t.pami0.train'

if not isinstance(path, list):
    path = [path]

for annotation_file in path:
    tmp = load_dataset_file(annotation_file)
    for s in tmp:
        seq_id = s["name"]
        if seq_id in samples:
            assert samples[seq_id]["name"] == s["name"]
            assert samples[seq_id]["signer"] == s["signer"]
            assert samples[seq_id]["gloss"] == s["gloss"]
            assert samples[seq_id]["text"] == s["text"]
            samples[seq_id]["sign"] = torch.cat(
                [samples[seq_id]["sign"], s["sign"]], axis=1
            )
        else:
            samples[seq_id] = {
                "name": s["name"],
                "signer": s["signer"],
                "gloss": s["gloss"],
                "text": s["text"],
                "sign": s["sign"],
            }

        print(samples[seq_id])
        print(samples[seq_id]["sign"].size())
        exit(0)
