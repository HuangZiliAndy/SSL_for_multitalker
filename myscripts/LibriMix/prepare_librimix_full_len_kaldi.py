# Data preparation for the LibriMix dataset

import os
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Prepare the LibriMix dataset')
parser.add_argument('text_file', type=str, help='Text file from Kaldi directory')
parser.add_argument('data_dir', type=str, help='LibriMix data directory')
parser.add_argument('output_dir', type=str, help='Output directory')
args = parser.parse_args()

def get_text(text_file):
    seg2text = {}
    with open(text_file, 'r') as fh:
        content = fh.readlines()
    for line in content:
        line = line.strip('\n')
        line_split = line.split(None, 1)
        seg2text[line_split[0]] = line_split[1]
    return seg2text

def main():
    seg2text = get_text(args.text_file)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    mix_files = os.listdir(args.data_dir)

    wav_scp_file = open("{}/wav.scp".format(args.output_dir), 'w')
    utt2spk_file = open("{}/utt2spk".format(args.output_dir), 'w')
    text_file = open("{}/text".format(args.output_dir), 'w')
    for mix_f in mix_files:
        utt = mix_f.split('.')[0]
        seg1, seg2 = utt.split('_')[0], utt.split('_')[1]
        spk1, spk2 = seg1.split('-')[0], seg2.split('-')[0]
        utt1, utt2 = "{}-{}".format(spk1, utt), "{}-{}".format(spk2, utt) 
        wav_scp_file.write("{} {}\n".format(utt1, "{}/{}".format(args.data_dir, mix_f)))
        wav_scp_file.write("{} {}\n".format(utt2, "{}/{}".format(args.data_dir, mix_f)))
        utt2spk_file.write("{} {}\n".format(utt1, spk1))
        utt2spk_file.write("{} {}\n".format(utt2, spk2))
        text_file.write("{} {}\n".format(utt1, seg2text[seg1]))
        text_file.write("{} {}\n".format(utt2, seg2text[seg2]))
    wav_scp_file.close()
    utt2spk_file.close()
    text_file.close()
    return 0

if __name__ == '__main__':
    main()
