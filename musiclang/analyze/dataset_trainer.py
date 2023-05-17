from transformers import Trainer, TrainingArguments, AutoModelWithLMHead, GPT2LMHeadModel, GPT2Config, \
    GPT2TokenizerFast
from transformers import TextDataset,DataCollatorForLanguageModeling
from transformers import AutoTokenizer, GPT2TokenizerFast
import os
import glob
from tokenizers import ByteLevelBPETokenizer


def load_dataset(train_path, val_path, tokenizer, block_size=1024):
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_path,
        block_size=block_size)

    val_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=val_path,
        block_size=block_size)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    return train_dataset, val_dataset, data_collator


def train_custom_tokenizer(input_file, output_directory, vocab_size=200, min_frequency=2):
    tokenizer = ByteLevelBPETokenizer()
    tokenizer.train(
        files=[input_file],
        vocab_size=vocab_size,
        min_frequency=min_frequency,
        special_tokens=["<s>", "</s>", "<unk>", "<mask>"],
    )
    os.makedirs(output_directory, exist_ok=True)
    tokenizer.save_model(output_directory)
    return tokenizer


class DatasetFinetuner:
    """
    Main class for training a musiclang LLM model from an existing model

    Examples
    --------
    Finetune existing musiclangLLM
    >>>from musiclang.analyze.dataset_trainer import DatasetFinetuner
    >>>from transformers import GPT2TokenizerFast, GPT2LMHeadModel
    >>>model_hub_name = "floriangardin/musiclang"
    >>>train_dataset = "locals/data/training/train.txt"
    >>>val_dataset = "locals/data/training/val.txt"
    >>>output_dir = "locals/data/training/model"

    >>>model = GPT2LMHeadModel.from_pretrained(model_hub_name)
    >>>tokenizer = GPT2TokenizerFast.from_pretrained(model_hub_name)
    >>>finetuner = DatasetFinetuner(model, tokenizer, train_dataset, val_dataset, output_dir)
    >>>model, tokenizer = finetuner.train()
    """
    def __init__(self, model, tokenizer, train_dataset, val_dataset, output_dir):
        """

        Parameters
        ----------
        model: HuggingFace model
        tokenizer: HuggingFace tokenizer
        train_dataset: str
            Path of the concatenated train file
        val_dataset: str
            Path of the concatenated test file
        output_dir: str
            Where to save the model
        """

        self.model = model
        self.tokenizer = tokenizer
        self.output_dir = output_dir
        self.train_dataset = train_dataset
        self.val_dataset = val_dataset

    def train(self, epochs=5, batch_size=16, warmup_steps=500, block_size=1024, eval_steps=800):

        train_dataset, val_dataset, data_collator = load_dataset(self.train_dataset, self.val_dataset,
                                                                 self.tokenizer, block_size)

        training_args = TrainingArguments(
            output_dir=self.output_dir,  # The output directory
            overwrite_output_dir=True,  # overwrite the content of the output directory
            num_train_epochs=epochs,  # number of training epochs
            per_device_train_batch_size=batch_size,  # batch size for training
            per_device_eval_batch_size=batch_size,  # batch size for evaluation
            eval_steps=eval_steps,  # Number of update steps between two evaluations.
            save_steps=eval_steps,  # after # steps model is saved
            warmup_steps=warmup_steps,  # number of warmup steps for learning rate scheduler
            prediction_loss_only=True,
            evaluation_strategy="epoch",
            do_eval=True
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
        )
        print('Will train the model')
        trainer.train()
        trainer.save_model()

        return self.model, self.tokenizer


class DatasetTrainer:
    """
    Train a LLM from scratch using a configuration
    """

    def __init__(self, config_model, config_tokenizer, train_dataset, val_dataset, output_dir):
        self.config_model = config_model
        self.output_dir = output_dir
        self.train_dataset = train_dataset
        self.config_tokenizer = config_tokenizer
        self.val_dataset = val_dataset
        self.model = None
        self.tokenizer = None

    def preprocess(self):
        tokenizer = train_custom_tokenizer(self.train_dataset, self.output_dir, **self.config_tokenizer)
        return tokenizer
    def train(self, epochs=5, batch_size=16, warmup_steps=500, block_size=1024, eval_steps=800):
        # Train the tokenizer
        self.tokenizer = self.preprocess()
        train_dataset, val_dataset, data_collator = load_dataset(self.train_dataset, self.val_dataset,
                                                                 self.tokenizer, block_size)

        # Train the model

        config = GPT2Config(vocab_size=len(self.tokenizer),
                            bos_token_id=self.tokenizer.bos_token_id,
                            eos_token_id=self.tokenizer.eos_token_id,
                            **self.config_model
                            )

        # Initialize a new GPT-2 model with the custom configuration
        self.model = GPT2LMHeadModel(config)

        training_args = TrainingArguments(
            output_dir=self.output_dir,  # The output directory
            overwrite_output_dir=True,  # overwrite the content of the output directory
            num_train_epochs=epochs,  # number of training epochs
            per_device_train_batch_size=batch_size,  # batch size for training
            per_device_eval_batch_size=batch_size,  # batch size for evaluation
            eval_steps=eval_steps,  # Number of update steps between two evaluations.
            save_steps=eval_steps,  # after # steps model is saved
            warmup_steps=warmup_steps,  # number of warmup steps for learning rate scheduler
            prediction_loss_only=True,
            evaluation_strategy="epoch",
            do_eval=True
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
        )

        trainer.train()
        trainer.save_model()

