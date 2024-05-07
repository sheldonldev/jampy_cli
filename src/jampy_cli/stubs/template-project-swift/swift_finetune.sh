CUDA_VISIBLE_DEVICES=0 swift sft \
    --model_type "minicpm-v-v2" \
    --sft_type "lora" \
    --batch_size "8" \
    --eval_batch_size "4" \
    --model_id_or_path "/home/sheldon/repos/MiniCPM/output/minicpm-v-v2/v3/checkpoint-2500-merged" \
    --template_type "minicpm-v" \
    --custom_train_dataset_path /home/sheldon/repos/MiniCPM/finetune/data/dec_table/train.json \
    --custom_val_dataset_path /home/sheldon/repos/MiniCPM/finetune/data/dec_table/dev.json \
    --save_steps "100" \
    --lora_target_modules q_proj k_proj v_proj \
    --learning_rate "1e-05" \
    --gradient_accumulation_steps "16" \
    --add_output_dir_suffix False \
    --output_dir /home/sheldon/repos/MiniCPM/output/minicpm-v-v2/v4 \
    --logging_dir /home/sheldon/repos/MiniCPM/output/minicpm-v-v2/v4/runs