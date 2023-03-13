import torch
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('input_path', type=str, help='Input path')
parser.add_argument('w2v_path', type=str, help='Pretrain model path')
parser.add_argument('output_path', type=str, help='Output path')
args = parser.parse_args()

def main():
    model = torch.load(args.input_path)
    model['cfg']['model']['w2v_path'] = args.w2v_path
    torch.save(model, args.output_path)
    return 0

if __name__ == '__main__':
    main()
