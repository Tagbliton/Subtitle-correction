# pip3 install transformers
# python3 deepseek_tokenizer.py
import transformers

def tokenizer(value):
        chat_tokenizer_dir = "./deepseek_v3_tokenizer/"

        tokenizer = transformers.AutoTokenizer.from_pretrained(
                chat_tokenizer_dir, trust_remote_code=True
                )

        result = tokenizer.encode(value)
        print(f"token {len(result)}")
        return len(result)

