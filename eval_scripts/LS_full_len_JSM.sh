source path.sh

fairseq_path=/export/c05/hzili1/projects/ICASSP23/fairseq_d01
export PYTHONPATH="${PYTHONPATH}:${fairseq_path}"

egs_path=$fairseq_path/examples/
data_dir=`pwd`/datasets/fairseq/LibriMix_full_len
exp_dir=`pwd`/experiment/LS_full_len/wavLM_spk_JSM
embed_dir=/export/c05/hzili1/SSL_multispk/embeddings/LS_enroll_15s/xvec
JSD=true
nspks=2
ckpt=checkpoint_last

for split in test_utt_group; do
  results_path=$exp_dir/decode/${ckpt}/LibriMix_${split}
  mkdir -p $results_path

  CUDA_VISIBLE_DEVICES=0 python $egs_path/speech_recognition/new/infer.py \
  	  --config-dir `pwd`/config/decode \
  	  --config-name infer_viterbi \
  	  task.data=$data_dir \
  	  task.normalize=false \
  	  task.embed_dir=$embed_dir \
  	  task.JSD=$JSD \
	  task.nspks=$nspks \
	  common_eval.results_path=$results_path \
	  common_eval.path=$exp_dir/checkpoints/${ckpt}.pt \
	  decoding.results_path=$results_path \
	  dataset.gen_subset=$split \
	  dataset.batch_size=1
done
