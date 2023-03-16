source path.sh

# Force alignment from https://github.com/s3prl/LibriMix/tree/master/metadata/LibriSpeech 
rttm_dir=/export/b06/hzili1/datasets/LibriSpeech_rttm/

# Follow https://github.com/kaldi-asr/kaldi to prepare text
# transcripts for LibriSpeech
kaldi_LS_dir=/export/c12/hzili1/tools/kaldi/egs/librispeech/s5/data/

# Follow https://github.com/JorisCos/LibriMix to prepare Libri2Mix
# Set librimix_dir to Libri2Mix/wav16k/max
librimix_dir=/export/c12/hzili1/dataset/LibriMix/Libri2Mix/wav16k/max/

# Output directories
kaldi_dir=datasets/kaldi/LibriMix
dump_dir=datasets/dump/LibriMix
fairseq_dir=datasets/fairseq/LibriMix

stage=1

# Prepare KALDI directory
if [ $stage -le 1 ]; then
  python myscripts/LibriMix/prepare_librimix_kaldi.py ${rttm_dir}/train_clean_100.rttm ${kaldi_LS_dir}/train_clean_100/text ${librimix_dir}/train-100/mix_clean ${kaldi_dir}/train-100
  utils/fix_data_dir.sh ${kaldi_dir}/train-100
  
  for split in dev test; do
    python myscripts/LibriMix/prepare_librimix_kaldi.py ${rttm_dir}/${split}_clean.rttm ${kaldi_LS_dir}/${split}_clean/text ${librimix_dir}/${split}/mix_clean ${kaldi_dir}/${split}
    utils/fix_data_dir.sh ${kaldi_dir}/${split}
  done
fi

# Dump segment files
if [ $stage -le 2 ]; then
  for split in train-100 dev test; do
    python myscripts/dump_segments.py ${kaldi_dir}/${split}/wav.scp $dump_dir/${split} --segments ${kaldi_dir}/${split}/segments 
    awk -F' ' '{print $1,$1}' $dump_dir/${split}/wav.scp > $dump_dir/${split}/utt2spk
    cp ${kaldi_dir}/${split}/text $dump_dir/${split}/.
    utils/fix_data_dir.sh $dump_dir/${split}
  done
fi

# Convert KALDI directory to fairseq format
if [ $stage -le 3 ]; then
  for split in train-100 dev test; do
    python myscripts/data_prep_kaldi.py ${dump_dir}/${split} $fairseq_dir $split $dump_dir/${split}/data
  done
  cp dict.ltr.txt $fairseq_dir/.
fi
