# Basic usage of GPT2 model

import gpt_2_simple as gpt2
import os
import requests

model_name = "124M"
file_name = "shakespeare.txt"

# download gpt2 model if not in path
if not os.path.isdir(os.path.join("models", model_name)):
	gpt2.download_gpt2(model_name=model_name)

# train from text file
if not os.path.isfile(file_name):
	data = requests.get("https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt")
	with open(file_name, "w") as f:
		f.write(data.text)

# exec
sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              file_name,
              model_name=model_name,
              steps=1000)

gpt2.generate(sess)