# Import Modules
import os
from datasets import load_dataset, interleave_datasets, DatasetDict
from huggingface_hub import login

# HuggingFace Hub Login
login(os.getenv('HF_TOKEN'))

# Load Seperate Training Dataset
wikipedia_nl_data = load_dataset("wikimedia/wikipedia", "20231101.nl", split = 'train').remove_columns(['id', 'url', 'title'])
mc4_nl_data = load_dataset('yhavinga/mc4_nl_cleaned', 'tiny', trust_remote_code = True, split = 'train').remove_columns(['timestamp', 'url'])
print(wikipedia_nl_data)
print(mc4_nl_data)

# Interleave Datasets
train_data = interleave_datasets([wikipedia_nl_data, mc4_nl_data], seed = 42)
print(train_data)

# Print Training Samples
print(train_data[0]['text'][:128])
print(train_data[1]['text'][:128])
print(train_data[2]['text'][:128])

# Test Data
test_data = load_dataset('yhavinga/mc4_nl_cleaned', 'tiny', trust_remote_code = True, split = 'validation').remove_columns(['timestamp', 'url'])
print(test_data)

# Print Training Samples
print(test_data[0]['text'][:128])

# Split train_data in 5 equal parts
num_splits = 5
split_size = len(train_data) // num_splits
splits = []

for i in range(num_splits):
    start_idx = i * split_size
    end_idx = (i + 1) * split_size if i != num_splits - 1 else len(train_data)
    splits.append(train_data.select(range(start_idx, end_idx)))

# Create a final dataset with train_data splits
final_ds = DatasetDict({f"train_{i+1}": split for i, split in enumerate(splits)})

# Also add test part
final_ds["test"] = test_data

# Summary
print(final_ds)

# Push to Hub - Private
final_ds.push_to_hub("robinsmits/pretrain_dataset_v1", private = True)