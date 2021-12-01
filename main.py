import argparse
import json
from pycocoevalcap.eval import ClipScore

#computes RefCLIPScore (CLIPScore augmented by the accessibility of a reference)

parser = argparse.ArgumentParser(allow_abbrev=False)
parser.add_argument('--src', type=str, metavar='N',
                    help='source file')
parser.add_argument('--hyp', type=str, metavar='N',
                    help='hypothesis file')
parser.add_argument('--refs', type=str, metavar='N',
                    help='reference file')
parser.add_argument('--outfile', type=str, metavar='N',
                    help='output file')
args = parser.parse_args()

def read_jsonl(infile, extract_key=None):
    f = open(infile, 'r')
    if extract_key is None:
        out = [json.loads(line.strip()) for line in f]
    else:
        out = [json.loads(line.strip())[extract_key] for line in f]
    f.close()
    return out

def get_image_id(image_name):
    # e.g. COCO_val2014_000000000974.jpg
    return (image_name.split('.')[0]).split('_')[2]

def score(src, hyp, refs, outfile):
    idx2Imgid = {idx: get_image_id(s) for idx, s in enumerate(read_jsonl(src, 'src'))}
    candidates = {idx2Imgid[idx]: [c] for idx, c in enumerate(read_jsonl(hyp, 'hyp'))}
    references = {idx2Imgid[idx]: c_refs for idx, c_refs in enumerate(read_jsonl(refs, 'refs'))}
    scorer = ClipScore()
    # scorer.compute_score(self, gts, res)
    # gts: {'image_id': [ref1, ref2, ...], ...}
    # res: {'image_id': [hyp], ...}
    average_score, idx2score = scorer.compute_score(references, candidates)
    with open(outfile, 'wt') as fout:
        for i in range(len(idx2score)):
            fout.write(str(idx2score[idx2Imgid[i]]['CLIPScore']))
            fout.write('\n')

if __name__ == '__main__':
    score(args.src, args.hyp, args.refs, args.outfile)
