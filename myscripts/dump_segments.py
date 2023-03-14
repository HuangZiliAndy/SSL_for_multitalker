import os
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Dump short segments')
parser.add_argument('wav_scp', type=str, help='wav.scp file')
parser.add_argument('output_dir', type=str, help='output directory')
parser.add_argument('--segments', type=str, default=None, help='segments file')
args = parser.parse_args()

def load_wav_scp(fname):
    utt2wav = {}
    with open(fname, 'r') as fh:
        content = fh.readlines()
    for line in content:
        line = line.strip('\n')
        line_split = line.split()
        assert len(line_split) == 2
        utt2wav[line_split[0]] = line_split[1]
    return utt2wav

def main():
    data_dir = args.output_dir + '/data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    utt2wav = load_wav_scp(args.wav_scp)

    if args.segments is not None:
        with open(args.segments, 'r') as fh:
            content = fh.readlines()

        wav_scp_file = open("{}/wav.scp".format(args.output_dir), 'w')
        for i in range(len(content)):
            line = content[i]
            line = line.strip('\n')
            line_split = line.split()
            seg, utt, start_t, end_t = line_split[0], line_split[1], round(float(line_split[2]), 2), round(float(line_split[3]), 2)
            output_audio = "{}/{}.wav".format(data_dir, seg)
            cmd = "sox {} {} trim {:.2f} {:.2f}".format(utt2wav[utt], output_audio, start_t, end_t-start_t)
            status, output = subprocess.getstatusoutput(cmd)
            assert status == 0
            wav_scp_file.write("{} {}\n".format(seg, output_audio))
            print("Finish {}/{}".format(i + 1, len(content)))
        wav_scp_file.close()
    else:
        uttlist = list(utt2wav.keys())
        uttlist.sort()

        wav_scp_file = open("{}/wav.scp".format(args.output_dir), 'w')
        for i in range(len(uttlist)):
            utt = uttlist[i]
            output_audio = "{}/{}.wav".format(data_dir, utt)
            cmd = "ln -s {} {}".format(utt2wav[utt], output_audio)
            status, output = subprocess.getstatusoutput(cmd)
            assert status == 0
            wav_scp_file.write("{} {}\n".format(utt, output_audio))
            print("Finish {}/{}".format(i + 1, len(uttlist)))
        wav_scp_file.close()
    return 0

if __name__ == '__main__':
    main()
