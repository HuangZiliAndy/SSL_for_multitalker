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
