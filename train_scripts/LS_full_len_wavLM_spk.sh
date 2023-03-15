source path.sh
echo `eval hostname`

train_subset=train-100
valid_subset=dev
embed_type=xvec
embed_dir=/export/c05/hzili1/SSL_multispk/embeddings/LS_enroll_15s/$embed_type
embed_dim=512
spk_method="None"
spk_layers='0'
cat_layers='0'
max_update=50000
lr=3e-5
apply_mask=false
keep_spk_layers=true
ln_after_adapt=false
cln=true
cln_bias=false
port=$((15388 + 12))
fp16=true
exp_dir=experiment/LS_full_len/wavLM_spk

CUDA_VISIBLE_DEVICES=0,1 fairseq-hydra-train \
	task.data=`pwd`/datasets/fairseq/LibriMix_full_len \
	task.label_dir=`pwd`/datasets/fairseq/LibriMix_full_len \
	task.embed_dir=$embed_dir \
	dataset.max_tokens=1200000 \
	dataset.train_subset=${train_subset} \
	dataset.valid_subset=${valid_subset} \
	distributed_training.distributed_world_size=2 \
	distributed_training.distributed_init_method='tcp://localhost:'${port} \
	optimization.lr=[$lr] \
	optimization.update_freq=[8] \
	optimization.max_update=${max_update} \
	model.apply_mask=$apply_mask \
        model.spk_aware=true \
	model.spk_embed=${embed_dim} \
        model.spk_method=${spk_method} \
	model.spk_layers=${spk_layers} \
	model.cat_layers=${cat_layers} \
	model.keep_spk_layers=${keep_spk_layers} \
	model.init_linear=true \
	model.ln_after_adapt=${ln_after_adapt} \
	model.cln=${cln} \
	model.cln_bias=${cln_bias} \
       	model.w2v_path=`pwd`/downloads/WavLM-Base+.pt \
	hydra.run.dir=${exp_dir} \
	common.fp16=${fp16} \
	--config-dir `pwd`/config \
	--config-name base
