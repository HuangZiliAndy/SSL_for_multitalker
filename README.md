We provide the code and models for our ICASSP paper [Adapting self-supervised models to multi-talker speech recognition using speaker embeddings](https://arxiv.org/abs/2211.00482).

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

Extract speaker embeddings for enrollment utterances. We use 15s speech from LibriVox (not in LibriSpeech) [LS 15 seconds enrollment](https://drive.google.com/file/d/1AmZQnTUCPW3VHZeYpBzH4fxExi_JBkv3/view?usp=share_link) as enrollment utterances. We also offer extracted [x-vector](https://drive.google.com/file/d/1kKVtXTtjwS0V4ZsYzj1863f9AXgLqMvP/view?usp=share_link) embeddings.

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
./train_scripts/LS_full_len_wavLM_spk.sh

# Utterance group-based evaluation (wavLM Base+ with speaker embedding + Joint Speaker Modeling (JSM))
./train_scripts/LS_full_len_wavLM_spk_JSM.sh
```

# Evaluation

``` bash
# Utterance-based evaluation with and w/o speaker embedding
./eval_scripts/LS.sh

# Utterance group-based evaluation (wavLM Base+ with speaker embedding)
./eval_scripts/LS_full_len.sh

# Utterance group-based evaluation (wavLM Base+ with speaker embedding + JSM)
./eval_scripts/LS_full_len_JSM.sh
```

# Pretrained models

[Utterance-based evaluation (wavLM Base+ without speaker embedding)](https://drive.google.com/file/d/1tMARaaR0YmgcJUEDVrnTFfNE2i68uC4W/view?usp=share_link)

[Utterance-based evaluation (wavLM Base+ with speaker embedding)](https://drive.google.com/file/d/1XcdxeSbWa6cQAfnUmlEg1YeWdndbDQTA/view?usp=share_link)

[Utterance group-based evaluation (wavLM Base+ with speaker embedding)](https://drive.google.com/file/d/1A3kXrXlyYDZhZVcHr_4NqjIjR4Kd9sgm/view?usp=share_link)

[Utterance group-based evaluation (wavLM Base+ with speaker embedding + JSM)](https://drive.google.com/file/d/1gb85DUNRs5Ep6HjLuVHOKWDka5LhK9KZ/view?usp=share_link)

When you are doing inference using the pretrained model, please first convert the model using

```python
python myscripts/convert_model.py <model_dir>/checkpoint_last.pt downloads/WavLM-Base+.pt <model_dir>/checkpoint_last_tmp.pt
mv <model_dir>/checkpoint_last_tmp.pt <model_dir>/checkpoint_last.pt
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
