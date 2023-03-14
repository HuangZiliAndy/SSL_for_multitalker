#!/usr/bin/env python

# This script creates *.ltr, *.wrd and *.tsv
# from a kaldi-style directory

import os
import sys
import argparse
import soundfile as sf

parser = argparse.ArgumentParser(description='Data preparation from a kaldi-style directory')
parser.add_argument('kaldi_dir', type=str, help='Kaldi style directory')
parser.add_argument('output_dir', type=str, help='Output directory')
parser.add_argument('output_name', type=str, help='Output name')
parser.add_argument('data_dir', type=str, help='Common data directory for audio files')
parser.add_argument('--min_sample', type=int, default=0)
parser.add_argument('--max_sample', type=int, default=10000000000)
args = parser.parse_args()

def process_file(fname):
    utt2info = {}
    with open(fname, 'r') as fh:
        content = fh.readlines()
    for line in content:
        line = line.strip('\n')
        line_split = line.split(None, 1)
        if len(line_split) == 2:
            utt2info[line_split[0]] = line_split[1]
        else:
            utt2info[line_split[0]] = ""
    return utt2info

def main():
    for f in ["wav.scp", "text"]:
        assert os.path.exists("{}/{}".format(args.kaldi_dir, f))
    utt2path, utt2text = process_file("{}/wav.scp".format(args.kaldi_dir)), process_file("{}/text".format(args.kaldi_dir))
    assert len(utt2path) == len(utt2text)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    uttlist = list(utt2path.keys())
    uttlist.sort()

    tsv_file = open("{}/{}.tsv".format(args.output_dir, args.output_name), 'w')
    ltr_file = open("{}/{}.ltr".format(args.output_dir, args.output_name), 'w')
    wrd_file = open("{}/{}.wrd".format(args.output_dir, args.output_name), 'w')
    tsv_file.write("{}\n".format(args.data_dir))
    cnt, cnt_success = 0, 0
    for utt in uttlist:
        cnt += 1
        file_path, text = utt2path[utt], utt2text[utt]
        num_samples = sf.info(file_path).frames
        if int(num_samples) < args.min_sample or int(num_samples) > args.max_sample:
            continue
        tsv_file.write("{}\t{}\n".format(os.path.relpath(file_path, args.data_dir), num_samples))
        wrd_out = " ".join(text.split())
        wrd_file.write("{}\n".format(wrd_out))
        ltr_out = " ".join(list(wrd_out.replace(" ", "|"))) + " |"
        ltr_file.write("{}\n".format(ltr_out))
        cnt_success += 1
    tsv_file.close()
    ltr_file.close()
    wrd_file.close()
    print("Keep {} of {} utterances".format(cnt_success, cnt))
    return 0

if __name__ == '__main__':
    main()
