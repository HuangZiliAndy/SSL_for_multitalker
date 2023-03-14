# Data preparation for the LibriMix dataset

import os
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Prepare the LibriMix dataset')
parser.add_argument('rttm_file', type=str, help='RTTM file from force alignment (from s3prl Jiatong)')
parser.add_argument('text_file', type=str, help='Text file from Kaldi directory')
parser.add_argument('data_dir', type=str, help='LibriMix data directory')
parser.add_argument('output_dir', type=str, help='Output directory')
args = parser.parse_args()

def get_start_end_time(rttm_file):
    seg2time = {}
    with open(rttm_file, 'r') as fh:
        content = fh.readlines()
    for line in content:
        line = line.strip('\n')
        line_split = line.split()
        segname, start_t, dur, spk = line_split[1], float(line_split[3]), float(line_split[4]), line_split[7]
        end_t = start_t + dur
        segname = spk + '-' + segname
        if segname not in seg2time:
            seg2time[segname] = []
        seg2time[segname].append([start_t, end_t])
    for seg in seg2time.keys():
        align = seg2time[seg]
        align = np.array(align)
        start_t, end_t = np.min(align), np.max(align)
        seg2time[seg] = [start_t, end_t]
    return seg2time

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
    seg2time = get_start_end_time(args.rttm_file)
    seg2text = get_text(args.text_file)
    assert len(seg2time) == len(seg2text)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    mix_files = os.listdir(args.data_dir)

    wav_scp_file = open("{}/wav.scp".format(args.output_dir), 'w')
    segments_file = open("{}/segments".format(args.output_dir), 'w')
    utt2spk_file = open("{}/utt2spk".format(args.output_dir), 'w')
    text_file = open("{}/text".format(args.output_dir), 'w')
    for mix_f in mix_files:
        utt = mix_f.split('.')[0]
        seg1, seg2 = utt.split('_')[0], utt.split('_')[1]
        spk1, spk2 = seg1.split('-')[0], seg2.split('-')[0]
        utt1, utt2 = "{}-{}".format(spk1, utt), "{}-{}".format(spk2, utt) 
        wav_scp_file.write("{} {}\n".format(utt, "{}/{}".format(args.data_dir, mix_f)))
        utt2spk_file.write("{} {}\n".format(utt1, spk1))
        utt2spk_file.write("{} {}\n".format(utt2, spk2))
        segments_file.write("{} {} {:.2f} {:.2f}\n".format(utt1, utt, seg2time[seg1][0], seg2time[seg1][1]))
        segments_file.write("{} {} {:.2f} {:.2f}\n".format(utt2, utt, seg2time[seg2][0], seg2time[seg2][1]))
        text_file.write("{} {}\n".format(utt1, seg2text[seg1]))
        text_file.write("{} {}\n".format(utt2, seg2text[seg2]))
    wav_scp_file.close()
    segments_file.close()
    utt2spk_file.close()
    text_file.close()
    return 0

if __name__ == '__main__':
    main()
