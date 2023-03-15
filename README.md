We provide the code and models for our ICASSP paper [Adapting self-supervised models to multi-talker speech recognition using speaker embeddings](https://arxiv.org/abs/2211.00482)

# Requirements and Installation
* Python version == 3.7
* torch==1.10.0, torchaudio==0.10.0

``` bash
# Install fairseq
git clone -b multispk --single-branch https://github.com/HuangZiliAndy/fairseq.git
cd fairseq
pip install --editable ./

# Install apex
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" \
  --global-option="--deprecated_fused_adam" --global-option="--xentropy" \

pip install -r requirements.txt 
```

# Data prepare

``` bash
# Prepare LibriMix (https://github.com/JorisCos/LibriMix)
# We only need 16k max condition in our experiment, and train-360
# is not needed.

# Install Kaldi (https://github.com/kaldi-asr/kaldi)

# Link utils to current directory
ln -s <kaldi_dir>/egs/wsj/s5/utils .

# Follow the following two scripts to prepare fairseq style
# training data for LibriMix

# The difference between the following two scripts is that
# the former makes use of force alignment results to create
# tight boundary (utterance-based evaluation)
./myscripts/LibriMix/prepare_librimix.sh
./myscripts/LibriMix/prepare_librimix_full_len.sh
```

# Training

Download [wavLM](https://github.com/microsoft/UniSpeech/tree/main/WavLM) models
and put it under downloads directory

We offer a few example scripts for training.

``` bash
# Utterance-based evaluation (wavLM Base+ without speaker embedding)
./train_scripts/LS_wavLM.sh

# Utterance-based evaluation (wavLM Base+ with speaker embedding)
./train_scripts/LS_wavLM_spk.sh

# Utterance group-based evaluation (wavLM Base+ with speaker embedding)
./train_scripts/LS_wavLM_spk.sh
```

# Evaluation

``` bash
Evaluation scripts for utterance-based evaluation and utterance group-based evaluation
./eval_scripts/LS_decode_viterbi.sh
./eval_scripts/LS_full_len_decode_viterbi.sh
```

# Citation

Please cite as:

``` bibtex
@inproceedings{huang2023adapting,
  title={Adapting self-supervised models to multi-talker speech recognition using speaker embeddings},
  author={Huang, Zili and Raj, Desh and Garc{\'\i}a, Paola and Khudanpur, Sanjeev},
  booktitle={IEEE ICASSP},
  year={2023},
}
```