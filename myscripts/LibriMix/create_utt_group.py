import os
import argparse

parser = argparse.ArgumentParser(description='Create utterance group for JSM')
parser.add_argument('data_dir', type=str, help='Fairseq data directory')
parser.add_argument('split', type=str, help='Data split')
args = parser.parse_args()

def main():
    with open("{}/{}.tsv".format(args.data_dir, args.split), 'r') as fh:
        content_tsv = fh.readlines()
    with open("{}/{}.ltr".format(args.data_dir, args.split), 'r') as fh:
        content_ltr = fh.readlines()
    assert len(content_tsv) == len(content_ltr) + 1

    common_dir = content_tsv[0]
    content_tsv = content_tsv[1:]

    utt2seginfo = {}
    for i in range(len(content_ltr)):
        text = content_ltr[i].strip('\n')
        tsv_line = content_tsv[i].strip('\n')
        audio_path, nsamples = tsv_line.split()[0], int(tsv_line.split()[1])
        segname = (audio_path.split('/')[-1]).split('.')[0]
        spk = segname.split('-')[0]
        uttname = '-'.join(segname.split('-')[1:])
        seginfo = [audio_path, nsamples, text, spk]
        if uttname not in utt2seginfo:
            utt2seginfo[uttname] = []
        utt2seginfo[uttname].append(seginfo)

    tsv_file = open("{}/{}_utt_group.tsv".format(args.data_dir, args.split), 'w')
    ltr_file = open("{}/{}_utt_group.ltr".format(args.data_dir, args.split), 'w')
    tsv_file.write(common_dir)
    uttlist = list(utt2seginfo.keys())
    uttlist.sort()
    for utt in uttlist:
        seginfo = utt2seginfo[utt]
        if len(seginfo) != 2:
            continue
        tsv_file.write("{}\t{}\n".format(seginfo[0][0], seginfo[0][1]))
        ltr = '#'.join(["({}) {}".format(seg[3], seg[2]) for seg in seginfo])
        ltr_file.write(ltr + '\n')
    tsv_file.close()
    ltr_file.close()
    return 0

if __name__ == '__main__':
    main()
